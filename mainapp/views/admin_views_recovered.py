import base64

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from ..models import TeamMember, InternDetails, ProductInfo, YTvideos, Homeimgs
from ._shared import validateUploadedImage


@login_required
def analysis(request):
    if request.user.username != 'atharva':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('/')
    return render(request, 'UserSection/analysis.html')


@login_required
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


@login_required
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

            try:
                validateUploadedImage(photo)
            except ValidationError as e:
                messages.error(request, str(e))
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


@login_required
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

            try:
                validateUploadedImage(photo)
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('add_intern')

            photo_base64 = "data:image/png;base64," + base64.b64encode(photo.read()).decode('utf-8')

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


@login_required
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
                validateUploadedImage(photo)
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


@login_required
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
                validateUploadedImage(imageFile)
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


@login_required
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

    # (slug, label) — science/craft renamed from Kids Science / Kids Craft
    product_categories = [
        ('softwareprojects', 'Software'),
        ('hardwareprojects', 'Hardware'),
        ('mechanicalprojects', 'Mechanical'),
        ('simulationprojects', 'Simulation'),
        ('science', 'Science'),
        ('craft', 'Craft'),
    ]
    return render(request, 'ProductSection/add_product.html', {'product_categories': product_categories})


@login_required
def edit_hero_images(request):
    if request.user.username != 'atharva':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('dashboard')

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
