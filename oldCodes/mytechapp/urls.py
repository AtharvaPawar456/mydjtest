from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit_hero_images/', views.edit_hero_images, name='edit_hero_images'),
    path('contactus/', views.contactus, name='contactus'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('ourteam/', views.our_team, name='our_team'),
    path('ourteam/profile/', views.team_member_profile, name='team_member_profile'),
    path('internship/', views.internship_listing, name='internship_listing'),
    path('internship/profile/<int:intern_id>/', views.intern_profile, name='intern_profile'),
    path('internship/opportunities/', views.internship_opportunities, name='internship_opportunities'),
    path('kids-projects/', views.kids_projects, name='kids_projects'),
    path('engineering-projects/', views.engineering_projects_category, name='engineering_projects_category'),
    path('youtube-projects/', views.youtube_projects, name='youtube_projects'),
    path('video-player/<int:video_id>/', views.video_player, name='video_player'),
    path('add-video/', views.add_video, name='add_video'),
    path('gallery/', views.gallery, name='gallery'),

    path('register/', views.register, name='register'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),

    # User --------------------------------------------
    path('userdashboard/', views.userdashboard, name='userdashboard'),
    path('profile/', views.profile, name='profile'),

    path('productlist/', views.productlist, name='productlist'),
    path('productinfo/<int:prod_id>/', views.productinfo, name='productinfo'),
    path('edit-product/<int:prod_id>/', views.edit_product, name='edit_product'),
    path('add-to-favorites/<int:prod_id>/', views.add_to_favorites, name='add_to_favorites'),


    path('earn-tasks/', views.activeEarnTasksView, name='active_earn_tasks'),
    path('earn-tasks/task/', views.earnTaskDetailView, name='task_detail'),

    path('affiliateinfo/', views.affiliateinfo, name='affiliateinfo'),
    # path('affiliateuser/task/', views.earnTaskDetailView, name='task_detail'),

    # Admin --------------------------------------------
    path('analysis/', views.analysis, name='analysis'),
    
    path('addproduct/', views.addproduct, name='addproduct'),
    path('uploadimg/', views.uploadimg, name='uploadimg'),
    path('add-developer/', views.add_developer, name='add_developer'),
    path('add-intern/', views.add_intern, name='add_intern'),
    path('edit-developer/<int:member_id>/', views.edit_developer, name='edit_developer'),
    # path('getproductdetails/', views.getproductdetails, name='getproductdetails'),
]
