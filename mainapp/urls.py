from django.urls import path
from django.views.generic import RedirectView
from . import views
from . import seo_views

urlpatterns = [
    path('robots.txt', seo_views.robots_txt, name='robots_txt'),
    path('sitemap.xml', seo_views.sitemap_xml, name='sitemap_xml'),

    path('', views.welcome, name='welcome'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit_hero_images/', views.edit_hero_images, name='edit_hero_images'),
    path('contactus/', views.contactus, name='contactus'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
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
    path('search/', views.global_search, name='global_search'),


    # Accessories
    path('accessories/', views.accessoriesProjects, name='accessories_projects'),
    path('accessoriesview/<int:apid>/', views.accessoriesView, name='accessories_view'),

    # aicontent
    path('aicontent/', views.aicontentList, name='aicontentlist'),
    path('aicontent/<int:aiid>/', views.aicontentView, name='aicontentview'),



    path('logout/', views.logoutView, name='logout'),

    # Legacy alias: /products used to 404 (real catalog is /productlist/)
    path(
        'products/',
        RedirectView.as_view(pattern_name='productlist', permanent=True),
        name='products_redirect',
    ),
    path(
        'products',
        RedirectView.as_view(pattern_name='productlist', permanent=True),
    ),
    path('productlist/', views.productlist, name='productlist'),
    # Category-scoped product pages (preferred)
    path(
        'productinfo/<slug:category_slug>/<int:prod_id>/',
        views.productinfo,
        name='productinfo',
    ),
    # Legacy: /productinfo/<id>/ redirects to category-scoped URL
    path('productinfo/<int:prod_id>/', views.productinfo, name='productinfo_legacy'),
    path(
        'edit-product/<slug:category_slug>/<int:prod_id>/',
        views.edit_product,
        name='edit_product',
    ),
    path('edit-product/<int:prod_id>/', views.edit_product, name='edit_product_legacy'),


    path('earn-tasks/', views.activeEarnTasksView, name='active_earn_tasks'),

    path('affiliateinfo/', views.affiliateinfo, name='affiliateinfo'),

    
    # Businesses
    path('allshops/', views.viewAllShop, name='viewallshop'),
    path('shop/<str:shopname>/', views.viewShop, name='viewshop'),
    

    # Admin --------------------------------------------
    path('analysis/', views.analysis, name='analysis'),
    
    path('addproduct/', views.addproduct, name='addproduct'),
    path('add-developer/', views.add_developer, name='add_developer'),
    path('add-intern/', views.add_intern, name='add_intern'),
    path('edit-developer/<int:member_id>/', views.edit_developer, name='edit_developer'),
    # path('getproductdetails/', views.getproductdetails, name='getproductdetails'),
]
