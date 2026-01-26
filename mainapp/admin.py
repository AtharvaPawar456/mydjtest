from django.contrib import admin

from .models import (
    UserDetails,
    UserFavProjects,
    Homeimgs,
    ProductInfo,
    Contactus,
    TeamMember,
    YTvideos,
    InternDetails,
    EarnTask,
    
    AccessoriesProd,
    AicontentProd,
    
    Businesswebinfo

)

admin.site.register(UserDetails)
admin.site.register(UserFavProjects)
admin.site.register(Homeimgs)
admin.site.register(ProductInfo)
admin.site.register(Contactus)
admin.site.register(TeamMember)
admin.site.register(YTvideos)
admin.site.register(InternDetails)
admin.site.register(EarnTask)

admin.site.register(AccessoriesProd)
admin.site.register(AicontentProd)

admin.site.register(Businesswebinfo)
