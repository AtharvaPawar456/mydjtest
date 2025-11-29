# from django.contrib import admin

# from .models import Contactus, ProductInfo, InternDetails

# admin.site.register(Contactus)
# admin.site.register(ProductInfo)
# admin.site.register(InternDetails)



from django.contrib import admin

from .models import (
    UserDetails,
    UserFavProjects,
    Homeimgs,
    ProductInfo,
    ProductImgs,
    ProductYT,
    Contactus,
    TeamMember,
    YTvideos,
    InternDetails,
    EarnTask
)

admin.site.register(UserDetails)
admin.site.register(UserFavProjects)
admin.site.register(Homeimgs)
admin.site.register(ProductInfo)
admin.site.register(ProductImgs)
admin.site.register(ProductYT)
admin.site.register(Contactus)
admin.site.register(TeamMember)
admin.site.register(YTvideos)
admin.site.register(InternDetails)
admin.site.register(EarnTask)
