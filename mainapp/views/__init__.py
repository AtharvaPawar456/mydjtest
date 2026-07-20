"""
mainapp view functions, split by domain.

Re-exported here so `from . import views` + `views.<name>` (used by urls.py)
keeps working exactly as it did when this was a single views.py file.
"""
from .system import welcome, dashboard, gallery, contactus, aboutus, logoutView
from .product import getQuickFilters, productlist, productinfo
from .search import global_search
from .legal import privacy_policy, terms_of_service
from .team import our_team, team_member_profile
from .intern import internship_listing, intern_profile, internship_opportunities
from .category import kids_projects, engineering_projects_category
from .youtube import youtube_projects, video_player
from .accessories import accessoriesProjects, accessoriesView
from .aicontent import aicontentList, aicontentView
from .earntask import activeEarnTasksView
from .affiliate import affiliateinfo
from .business import viewAllShop, viewShop
from .admin_views import (
    analysis, add_video, add_developer, add_intern, edit_developer,
    edit_product, addproduct, edit_hero_images,
)
