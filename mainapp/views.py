

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


import io, base64, time, os, string, secrets
from PIL import Image, ImageDraw
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


from .models import UserDetails, Contactus, ProductInfo, ProductImgs, ProductYT, TeamMember, UserFavProjects, YTvideos, InternDetails, Homeimgs, EarnTask





# --------------------------------------------------
# System Views
# --------------------------------------------------


def welcome(request):
    return render(request, 'systemsetup/welcome.html')

def dashboard(request):
    home_images = Homeimgs.objects.order_by('?')[:10]
    return render(request, 'systemsetup/herosection.html', {'home_images': home_images})

def gallery(request):
    galleryImgs = Homeimgs.objects.order_by('?')
    # get all images randomly
    return render(request, 'systemsetup/gallery.html', {'galleryImgs': galleryImgs})


@login_required(login_url='/login')
def contactus(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name", "").strip()
            email = request.POST.get("email", "").strip()
            message = request.POST.get("message", "").strip()

            if not name or not email or not message:
                messages.error(request, "All fields are required.")
                return redirect('contactus')
            fullMessage = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"

            Contactus.objects.create(name=name, emailid=email, msg=fullMessage)
            messages.success(request, "Your message has been sent successfully!")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect('contactus')
    return render(request, 'systemsetup/contactus.html')

def aboutus(request):
    return render(request, 'systemsetup/aboutus.html')

def generateUniqueRefId():
    """
    Generate a unique 8-character alphanumeric referral ID.
    Checks against the UserDetails model to ensure uniqueness.
    """
    characters = string.ascii_letters + string.digits
    while True:
        refId = ''.join(secrets.choice(characters) for _ in range(8))
        if not UserDetails.objects.filter(refid=refId).exists():
            return refId

def register(request):
    if request.method == 'POST':
        username    = request.POST.get('username', '').strip()
        address     = request.POST.get('address', '').strip()
        contact     = request.POST.get('contact', '').strip()
        email       = request.POST.get('email', '').strip()
        password   = request.POST.get('password', '')

        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)

                # Create corresponding UserDetails record
                UserDetails.objects.create(
                    user=user,
                    address=address if address else "*",
                    contactno=contact if contact else "*",
                    refid=str(generateUniqueRefId())
                )

                login(request, user)
                return redirect('/userdashboard')
            except Exception as e:
                messages.error(request, f'Error creating user: {e}')

    return render(request, 'systemsetup/register.html')

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Both fields are required.')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/userdashboard')
            else:
                messages.error(request, 'Invalid credentials.')

    return render(request, 'systemsetup/login.html')


def logoutView(request):
    logout(request)
    return redirect('/')








# --------------------------------------------------
# User Views
# --------------------------------------------------

from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def userdashboard(request):
    new_projects = ProductInfo.objects.all().order_by('-timestamp')[:6]
    context = {
        'new_projects': new_projects,
    }
    return render(request, 'UserSection/userdashboard.html', context)

def generateGradientImage():
    """
    Generates a gradient image (RGB) in memory and returns it as base64 string.
    """
    width, height = 300, 300
    image = Image.new('RGB', (width, height), color=0)

    draw = ImageDraw.Draw(image)
    for i in range(height):
        r = int(255 * (i / height))
        g = int(128 + 127 * (i / height))
        b = 255 - r
        draw.line([(0, i), (width, i)], fill=(r, g, b))

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    base64Image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return base64Image

@login_required(login_url='/login')
def profile(request):
    profileImage = generateGradientImage()
    user_details = get_object_or_404(UserDetails, user=request.user)
    context = {
        'profileImage': profileImage, 
        'user': request.user,
        'user_details': user_details
    }
    return render(request, 'UserSection/profile.html', context)

# def productlist(request):
#     """Fetches all / products by category from DB and renders them to the template."""
#     try:
#         category = request.GET.get('productcat')
#         if category:
#             productList = ProductInfo.objects.filter(productcat=category).order_by('-timestamp')
#         else:
#             productList = ProductInfo.objects.all().order_by('-timestamp')
#         return render(request, 'ProductSection/productlist.html', {'productList': productList})
#     except Exception as e:
#         return render(request, 'ProductSection/productlist.html', {'error': str(e)})


def productlist(request):
    """
    Fetches products from DB filtered by category or search query.
    Input:
        GET params:
            - productcat: filter by category (optional)
            - q: search term (optional)
    Working:
        Filters ProductInfo queryset based on category and/or search term 
        matching productname, prodtags, highlighttitle, or prodinfo.
    Output:
        Renders 'productlist.html' with filtered product list or error message.
    """
    try:
        category = request.GET.get('productcat', '').strip()
        searchQuery = request.GET.get('q', '').strip()

        productList = ProductInfo.objects.all()

        if category:
            productList = productList.filter(productcat__icontains=category)

        if searchQuery:
            productList = productList.filter(
                Q(productname__icontains=searchQuery) |
                Q(prodtags__icontains=searchQuery) |
                Q(highlighttitle__icontains=searchQuery) |
                Q(prodinfo__icontains=searchQuery)
            )

        productList = productList.order_by('-timestamp')

        return render(request, 'ProductSection/productlist.html', {
            'productList': productList,
            'productListcount': len(productList),
            'searchQuery': searchQuery
        })

    except Exception as e:
        return render(request, 'ProductSection/productlist.html', {
            'error': str(e)
        })


def productinfo(request, prod_id):
    try:
        product = get_object_or_404(ProductInfo, prodid=prod_id)
        productImages = ProductImgs.objects.filter(prod=product)
        productYTlinks = ProductYT.objects.filter(prod=product)
        is_favorite = False
        if request.user.is_authenticated:
            is_favorite = UserFavProjects.objects.filter(user=request.user, prod=product).exists()
        return render(request, 'ProductSection/productinfo.html', {
            'product': product,
            'productImages': productImages,
            'productYTlinks': productYTlinks,
            'is_favorite': is_favorite,
        })
    except Exception as e:
        return render(request, 'ProductSection/productinfo.html', {'error': str(e)})

@login_required(login_url='/login')
def add_to_favorites(request, prod_id):
    product = get_object_or_404(ProductInfo, prodid=prod_id)
    fav, created = UserFavProjects.objects.get_or_create(user=request.user, prod=product)
    if not created:
        fav.delete()
    return redirect('productinfo', prod_id=prod_id)


### Team Views

def our_team(request):
    team_members = TeamMember.objects.all().order_by('timestamp')
    return render(request, 'TeamSection/ourteam.html', {'team_members': team_members})

def team_member_profile(request):
    name = request.GET.get('name')
    member = None
    if name:
        try:
            member = TeamMember.objects.get(name__iexact=name)
        except TeamMember.DoesNotExist:
            member = None
    if not member:
        return render(request, 'TeamSection/ourteam_profile.html', {'member': None, 'error': 'Team member not found.'})
    return render(request, 'TeamSection/ourteam_profile.html', {'member': member})


### Internship Views

def internship_listing(request):
    interns = InternDetails.objects.all().order_by('-timestamp')
    return render(request, 'InternSection/internship_listing.html', {'interns': interns})

def intern_profile(request, intern_id):
    intern = get_object_or_404(InternDetails, internid=intern_id)
    return render(request, 'InternSection/intern_profile.html', {'intern': intern})

def internship_opportunities(request):
    return render(request, 'InternSection/internship_opportunities.html')



### Project Category Views


def kids_projects(request):
    return render(request, 'projectscategory/kids_projects.html')

def engineering_projects_category(request):
    return render(request, 'projectscategory/engineering_projects_category.html')

### Youtube Views

def youtube_projects(request):
    videos = YTvideos.objects.all().order_by('-timestamp')
    for video in videos:
        if 'v=' in video.videolink:
            video.embed_id = video.videolink.split('v=')[-1].split('&')[0]
        else:
            video.embed_id = ''
    return render(request, 'YoutubeSection/youtube_projects.html', {'videos': videos})

def video_player(request, video_id):
    video = get_object_or_404(YTvideos, ytid=video_id)
    # Extract video ID from link like 'https://www.youtube.com/watch?v=VIDEO_ID'
    embed_id = video.videolink.split('v=')[-1]
    context = {
        'video': video,
        'embed_id': embed_id
    }
    return render(request, 'YoutubeSection/video_player.html', context)

### EarnTask Views

def activeEarnTasksView(request):
    """
    Displays all active EarnTask records in descending timestamp order.
    io: request -> renders 'active_earn_tasks.html' with tasks context
    """
    try:
        activeTasks = EarnTask.objects.filter(estatus="active").order_by('-timestamp')
    except Exception as error:
        activeTasks = []
        print("Error fetching EarnTasks:", error)
    
    return render(request, 'earnTasks/active_earn_tasks.html', {'tasks': activeTasks})


def earnTaskDetailView(request):
    """
    Shows task details of selected task and lists 5 recent active tasks.
    io: request with taskno -> renders 'task_detail.html' with task and otherTasks
    """
    taskId = request.GET.get("taskno")
    selectedTask = None
    otherTasks = []

    try:
        selectedTask = get_object_or_404(EarnTask, etid=taskId)
        otherTasks = EarnTask.objects.filter(estatus="active").exclude(etid=taskId).order_by('-timestamp')[:5]
    except Exception as error:
        print("Error loading task detail:", error)
    
    return render(request, 'earnTasks/task_detail.html', {
        'task': selectedTask,
        'otherTasks': otherTasks
    })


### affiliate Views
def affiliateinfo(request):
    # Commission tiers: (upperLimit, rewardAmount)
    commissionTiers = [
        {"rangeMin": 0, "rangeMax": 2500, "reward": 100},
        {"rangeMin": 2500, "rangeMax": 3500, "reward": 150},
        {"rangeMin": 3500, "rangeMax": 5500, "reward": 200},
        {"rangeMin": 5500, "rangeMax": 6500, "reward": 300},
        {"rangeMin": 6500, "rangeMax": 7500, "reward": 350},
        {"rangeMin": 7500, "rangeMax": 9500, "reward": 450},
        {"rangeMin": 9500, "rangeMax": 10000, "reward": 500},
        {"rangeMin": 10000, "rangeMax": 12000, "reward": 1000}
    ]

    return render(request, 'AffiliateProgram/affiliateInfo.html', {
        "commissionTiers": commissionTiers
    })


# --------------------------------------------------
# Admin Views
# --------------------------------------------------

@login_required(login_url='/login')
def analysis(request):
    if request.user.username != 'atharva':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('/')
    return render(request, 'UserSection/analysis.html')



@login_required(login_url='/login')
def add_video(request):
    if request.user.username != 'atharva':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('youtube_projects')

    if request.method == 'POST':
        title = request.POST.get('videotitle')
        link = request.POST.get('videolink')

        if not title or not link:
            messages.error(request, "Both title and link are required.")
            return render(request, 'YoutubeSection/add_video.html')

        if 'youtube.com/watch?v=' not in link:
            messages.error(request, "Please provide a valid YouTube video link.")
            return render(request, 'YoutubeSection/add_video.html')

        try:
            YTvideos.objects.create(videotitle=title, videolink=link)
            messages.success(request, "Video added successfully!")
            return redirect('youtube_projects')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    return render(request, 'YoutubeSection/add_video.html')


@login_required(login_url='/login')
def add_developer(request):
    if request.user.username != 'atharva':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('/ourteam')
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            role = request.POST.get('role')
            experience = request.POST.get('experience')
            metadata = request.POST.get('metadata')
            photo = request.FILES.get('photo')
            linkedin_url = request.POST.get('linkedin_url')
            github_url = request.POST.get('github_url')

            if not all([name, role, experience, metadata, photo]):
                messages.error(request, "All fields except social links are required.")
                return redirect('add_developer')

            photo_base64 = base64.b64encode(photo.read()).decode('utf-8')

            TeamMember.objects.create(
                name=name,
                role=role,
                experience=experience,
                metadata=metadata,
                photo_base64="data:image/png;base64," + photo_base64,
                linkedin_url=linkedin_url,
                github_url=github_url
            )
            messages.success(request, "Team member added successfully!")
            return redirect('add_developer')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add_developer')

    return render(request, 'TeamSection/add_developer.html')


@login_required(login_url='/login')
def add_intern(request):
    if request.user.username != 'atharva':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('internship_listing')

    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            role = request.POST.get('role')
            experience = request.POST.get('experience')
            metadata = request.POST.get('metadata')
            photo = request.FILES.get('photo')
            linkedin_url = request.POST.get('linkedin_url')
            github_url = request.POST.get('github_url')

            if not all([name, role, experience, metadata, photo]):
                messages.error(request, "All fields except social links are required.")
                return redirect('add_intern')

            photo_base64 = base64.b64encode(photo.read()).decode('utf-8')

            InternDetails.objects.create(
                name=name,
                role=role,
                experience=experience,
                metadata=metadata,
                photo_base64=photo_base64,
                linkedin_url=linkedin_url,
                github_url=github_url
            )
            messages.success(request, "Intern added successfully!")
            return redirect('internship_listing')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add_intern')

    return render(request, 'InternSection/add_intern.html')


@login_required(login_url='/login')
def edit_developer(request, member_id):
    if request.user.username != 'atharva':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('/ourteam')

    member = get_object_or_404(TeamMember, pk=member_id)

    if request.method == 'POST':
        try:
            member.name = request.POST.get('name', member.name)
            member.role = request.POST.get('role', member.role)
            member.experience = request.POST.get('experience', member.experience)
            member.metadata = request.POST.get('metadata', member.metadata)
            member.linkedin_url = request.POST.get('linkedin_url', member.linkedin_url)
            member.github_url = request.POST.get('github_url', member.github_url)

            photo = request.FILES.get('photo')
            if photo:
                member.photo_base64 = "data:image/png;base64," + base64.b64encode(photo.read()).decode('utf-8')


            member.save()
            messages.success(request, "Team member details updated successfully!")
            return redirect('our_team')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('edit_developer', member_id=member_id)

    context = {
        'member': member
    }
    return render(request, 'TeamSection/edit_developer.html', context)






@login_required(login_url='/login')
def edit_product(request, prod_id):
    if request.user.username != 'atharva':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('productinfo', prod_id=prod_id)

    product = get_object_or_404(ProductInfo, prodid=prod_id)

    if request.method == 'POST':
        try:
            product.productname = request.POST.get('productname', product.productname)
            product.productcat = request.POST.get('productcat', product.productcat)
            product.highlighttitle = request.POST.get('highlighttitle', product.highlighttitle)
            product.prodinfo = request.POST.get('prodinfo', product.prodinfo)

            imageFile = request.FILES.get('mainimgfile')
            if imageFile:
                product.mainimgbasetxt = base64.b64encode(imageFile.read()).decode('utf-8')

            product.save()
            messages.success(request, "Product details updated successfully!")
            return redirect('productinfo', prod_id=prod_id)
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('edit_product', prod_id=prod_id)

    context = {
        'product': product
    }
    return render(request, 'ProductSection/edit_product.html', context)


@login_required(login_url='/login')
def addproduct(request):
    if request.user.username != 'atharva':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('/productlist')
    if request.method == 'POST':
        try:
            productName     = request.POST.get('productname', '*')
            productCategory = request.POST.get('productcat', '*')
            highlightTitle  = request.POST.get('highlighttitle', '*')
            prodinfo        = request.POST.get('prodinfo', '*')
            mainImgBaseTxt  = request.POST.get('mainimgfile', '*')
            prodtags        = request.POST.get('prodtags', '*')

            # # Handle uploaded file
            # imageFile       = request.FILES.get('mainimgfile')
            # mainImgBaseTxt  = "*"

            # if imageFile:
            #     imageBytes = imageFile.read()
            #     mainImgBaseTxt = base64.b64encode(imageBytes).decode('utf-8')

            # Save to DB
            ProductInfo.objects.create(
                productname=productName,
                productcat=productCategory,
                mainimgbasetxt=mainImgBaseTxt,
                prodtags=prodtags,

                highlighttitle=highlightTitle,
                prodinfo=prodinfo
            )
            messages.success(request, "Product added successfully!")
            return redirect('/addproduct')

        except Exception as error:
            messages.error(request, f"Error: {str(error)}")

    product_categories = [
        'softwareprojects',
        'hardwareprojects',
        'mechanicalprojects',
        'simulationprojects',
        'kidsscience',
        'kidscraft',
        # 'origami',
    ]
    return render(request, 'ProductSection/add_product.html', {'product_categories': product_categories})



@login_required(login_url='/login')
def uploadimg(request):
    if request.user.username != 'atharva':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('/productlist')
    if request.method == 'POST':
        try:
            prodid = request.POST.get('prodid')
            imageFile = request.FILES.get('imageFile')

            if not (prodid and imageFile):
                messages.error(request, "Product ID and image are required.")
                return redirect('uploadProductImg')

            productRef = ProductInfo.objects.get(prodid=prodid)
            base64Image = base64.b64encode(imageFile.read()).decode('utf-8')

            newImg = ProductImgs(
                prodid=productRef,
                productname=productRef.productname,
                highlighttitle=productRef.highlighttitle,
                mainimgbasetxt=base64Image
            )
            newImg.save()
            messages.success(request, "Image uploaded successfully.")
            return redirect('/uploadimg')

        except ProductInfo.DoesNotExist:
            messages.error(request, "Invalid Product ID.")
        except Exception as e:
            messages.error(request, f"Unexpected error: {str(e)}")

    products = ProductInfo.objects.all()
    return render(request, 'ProductSection/uploadImg.html', {'products': products})

@login_required
def edit_hero_images(request):
    if request.user.username != 'atharva':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('/HeroSection')

    if request.method == 'POST':
        if 'add_image' in request.POST:
            img_title = request.POST.get('imgtitle')
            img_link = request.POST.get('imglink')
            if img_title and img_link:
                Homeimgs.objects.create(imgtitle=img_title, imglink=img_link)
        elif 'delete_image' in request.POST:
            img_id = request.POST.get('img_id')
            if img_id:
                try:
                    image_to_delete = Homeimgs.objects.get(hiid=img_id)
                    image_to_delete.delete()
                except Homeimgs.DoesNotExist:
                    pass
        return redirect('edit_hero_images')

    images = Homeimgs.objects.all()
    return render(request, 'systemsetup/edit_hero_images.html', {'images': images})

