from django.contrib import admin
from django.http import HttpResponseNotAllowed
from django.middleware.csrf import get_token
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Homeimgs,
    ProductInfo,
    ProductCategory,
    Project_Software,
    Project_Hardware,
    Project_Mechanical,
    Project_Simulation,
    Project_Science,
    Project_Craft,
    Contactus,
    TeamMember,
    YTvideos,
    InternDetails,
    InternOpportunity,
    EarnTask,
    AccessoriesProd,
    AicontentProd,
    Businesswebinfo,
)
from .product_catalog import get_product_model

@admin.register(Homeimgs)
class HomeimgsAdmin(admin.ModelAdmin):
    list_display = ("hiid", "imgtitle", "imglink_short", "is_visible_display", "timestamp")
    search_fields = ("imgtitle", "imglink")
    list_filter = ("timestamp",)
    ordering = ("-timestamp",)
    readonly_fields = ("timestamp",)
    fieldsets = (
        (
            "Image",
            {
                "fields": ("imgtitle", "imglink"),
                "description": (
                    'Visibility: if Imgtitle is empty or "*", the image is hidden from hero/gallery. '
                    "Set a real title to make it visible. Imglink must be a real URL (not empty/*)."
                ),
            },
        ),
        ("Meta", {"fields": ("timestamp",)}),
    )

    @admin.display(description="Imglink", ordering="imglink")
    def imglink_short(self, obj):
        link = (obj.imglink or "").strip()
        if not link or link == "*":
            return "—"
        if len(link) > 60:
            return f"{link[:57]}..."
        return link

    @admin.display(description="Visible", boolean=True)
    def is_visible_display(self, obj):
        return obj.is_visible


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("catid", "name", "slug", "sort_order", "is_active", "product_count", "timestamp")
    list_editable = ("sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "slug", "legacy_slugs", "hashtags")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("sort_order", "name")
    readonly_fields = ("timestamp",)
    fieldsets = (
        (None, {"fields": ("name", "slug", "sort_order", "is_active")}),
        ("Aliases & filters", {"fields": ("legacy_slugs", "hashtags", "description")}),
        ("Meta", {"fields": ("timestamp",)}),
    )

    @admin.display(description="Products")
    def product_count(self, obj):
        Model = get_product_model(obj.slug)
        return Model.objects.count() if Model else 0


class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ("prodid", "productname", "prodcost", "timestamp")
    search_fields = ("productname", "prodtags", "highlighttitle")
    ordering = ("-timestamp",)
    readonly_fields = ("timestamp",)


@admin.register(Project_Software)
class ProjectSoftwareAdmin(CategoryProductAdmin):
    pass


@admin.register(Project_Hardware)
class ProjectHardwareAdmin(CategoryProductAdmin):
    pass


@admin.register(Project_Mechanical)
class ProjectMechanicalAdmin(CategoryProductAdmin):
    pass


@admin.register(Project_Simulation)
class ProjectSimulationAdmin(CategoryProductAdmin):
    pass


@admin.register(Project_Science)
class ProjectScienceAdmin(CategoryProductAdmin):
    pass


@admin.register(Project_Craft)
class ProjectCraftAdmin(CategoryProductAdmin):
    pass


# Legacy unified table (read-only-ish until data migration completes)
@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ("prodid", "productname", "productcat", "category", "timestamp")
    search_fields = ("productname", "productcat")
    ordering = ("-timestamp",)
    readonly_fields = ("timestamp",)


admin.site.register(Contactus)
admin.site.register(TeamMember)
admin.site.register(YTvideos)
admin.site.register(EarnTask)


@admin.register(InternDetails)
class InternDetailsAdmin(admin.ModelAdmin):
    list_display = (
        "internid",
        "name",
        "role",
        "is_stipend",
        "stipend_toggle",
        "timestamp",
    )
    list_filter = ("is_stipend",)
    search_fields = ("name", "role", "experience")
    list_editable = ("is_stipend",)
    ordering = ("-timestamp",)
    actions = ("mark_stipend", "mark_unstipend")
    readonly_fields = ("timestamp",)

    fieldsets = (
        ("Stipend", {"fields": ("is_stipend",)}),
        ("Profile", {"fields": ("name", "role", "experience", "photo_base64", "metadata")}),
        ("Links", {"fields": ("linkedin_url", "github_url", "applicationlink", "certificatelink")}),
        ("Meta", {"fields": ("timestamp",)}),
    )

    def changelist_view(self, request, extra_context=None):
        self.request = request
        return super().changelist_view(request, extra_context)

    @admin.display(description="Stipend / Unstipend")
    def stipend_toggle(self, obj):
        if obj.is_stipend:
            label = "Set Unstipend"
            color = "#b45309"
            bg = "#fef3c7"
        else:
            label = "Set Stipend"
            color = "#047857"
            bg = "#d1fae5"
        toggle_url = reverse("admin:interndetails_toggle_stipend", args=[obj.pk])
        return format_html(
            '<form action="{}" method="post" style="display:inline;">'
            '<input type="hidden" name="csrfmiddlewaretoken" value="{}">'
            '<button type="submit" class="button" style="padding:4px 10px;border-radius:6px;'
            'border:none;cursor:pointer;background:{};color:{};font-weight:600;">{}</button>'
            '</form>',
            toggle_url,
            get_token(self.request),
            bg,
            color,
            label,
        )

    @admin.action(description="Mark selected as STIPEND (paid)")
    def mark_stipend(self, request, queryset):
        n = queryset.update(is_stipend=True)
        self.message_user(request, f"{n} intern(s) marked as stipend.")

    @admin.action(description="Mark selected as UNSTIPEND (unpaid)")
    def mark_unstipend(self, request, queryset):
        n = queryset.update(is_stipend=False)
        self.message_user(request, f"{n} intern(s) marked as unstipend.")

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom = [
            path(
                "<path:object_id>/toggle-stipend/",
                self.admin_site.admin_view(self.toggle_stipend),
                name="interndetails_toggle_stipend",
            ),
        ]
        return custom + urls

    def toggle_stipend(self, request, object_id):
        from django.contrib import messages
        from django.shortcuts import redirect

        if request.method != "POST":
            return HttpResponseNotAllowed(["POST"])

        obj = self.get_object(request, object_id)
        if obj is None:
            messages.error(request, "Intern not found.")
            return redirect("admin:mainapp_interndetails_changelist")
        obj.is_stipend = not obj.is_stipend
        obj.save(update_fields=["is_stipend"])
        state = "stipend (paid)" if obj.is_stipend else "unstipend (unpaid)"
        messages.success(request, f"“{obj.name}” is now {state}.")
        return redirect("admin:mainapp_interndetails_changelist")
admin.site.register(AccessoriesProd)
admin.site.register(AicontentProd)


@admin.register(InternOpportunity)
class InternOpportunityAdmin(admin.ModelAdmin):
    list_display = (
        "opid",
        "title",
        "track",
        "mode",
        "is_stipend",
        "is_visible",
        "timestamp",
    )
    list_filter = ("is_visible", "is_stipend", "track", "mode")
    search_fields = ("title", "track", "skills", "description", "stipend")
    list_editable = ("is_visible", "is_stipend")
    ordering = ("opid",)
    actions = ("mark_visible", "mark_hidden", "mark_stipend", "mark_unstipend")
    readonly_fields = ("timestamp",)

    fieldsets = (
        ("Visibility", {"fields": ("is_visible", "is_stipend")}),
        (
            "Role",
            {"fields": ("opid", "title", "track", "mode", "duration", "stipend", "skills", "description")},
        ),
        ("Meta", {"fields": ("timestamp",)}),
    )

    @admin.action(description="Mark selected as VISIBLE")
    def mark_visible(self, request, queryset):
        updated = queryset.update(is_visible=True)
        self.message_user(request, f"{updated} opportunity(ies) set to visible.")

    @admin.action(description="Mark selected as HIDDEN")
    def mark_hidden(self, request, queryset):
        updated = queryset.update(is_visible=False)
        self.message_user(request, f"{updated} opportunity(ies) set to hidden.")

    @admin.action(description="Mark selected as STIPEND (paid)")
    def mark_stipend(self, request, queryset):
        updated = queryset.update(is_stipend=True)
        self.message_user(request, f"{updated} opportunity(ies) set to stipend.")

    @admin.action(description="Mark selected as UNSTIPEND (unpaid)")
    def mark_unstipend(self, request, queryset):
        updated = queryset.update(is_stipend=False)
        self.message_user(request, f"{updated} opportunity(ies) set to unstipend.")


@admin.register(Businesswebinfo)
class BusinesswebinfoAdmin(admin.ModelAdmin):
    list_display = (
        "bid",
        "bname",
        "bcat",
        "is_visible",
        "visibility_toggle",
        "public_link",
        "btimestamp",
    )
    list_filter = ("is_visible", "bcat")
    search_fields = ("bname", "bcat", "btags", "bhighlight")
    list_editable = ("is_visible",)
    ordering = ("-btimestamp",)
    actions = ("mark_visible", "mark_hidden")
    readonly_fields = ("btimestamp",)

    fieldsets = (
        ("Visibility", {"fields": ("is_visible",)}),
        ("Identity", {"fields": ("bname", "bcat", "btags", "bmainimg")}),
        ("Copy", {"fields": ("bhighlight", "binfo")}),
        ("Media", {"fields": ("bownerimgs", "bgallery")}),
        ("Links", {"fields": ("bweblinks", "bytlinks")}),
        ("Meta", {"fields": ("btimestamp",)}),
    )

    def changelist_view(self, request, extra_context=None):
        self.request = request
        return super().changelist_view(request, extra_context)

    @admin.display(description="View / Hide")
    def visibility_toggle(self, obj):
        """One-click button to flip public visibility."""
        if obj.is_visible:
            label = "Hide"
            color = "#b91c1c"
            bg = "#fee2e2"
        else:
            label = "View (show)"
            color = "#047857"
            bg = "#d1fae5"
        toggle_url = reverse("admin:businesswebinfo_toggle_visibility", args=[obj.pk])
        return format_html(
            '<form action="{}" method="post" style="display:inline;">'
            '<input type="hidden" name="csrfmiddlewaretoken" value="{}">'
            '<button type="submit" class="button" style="padding:4px 10px;border-radius:6px;'
            'border:none;cursor:pointer;background:{};color:{};font-weight:600;">{}</button>'
            '</form>',
            toggle_url,
            get_token(self.request),
            bg,
            color,
            label,
        )

    @admin.display(description="Public page")
    def public_link(self, obj):
        if not obj.bname or obj.bname == "*":
            return "—"
        return format_html(
            '<a href="/shop/{}/" target="_blank">Open</a>',
            obj.bname,
        )

    @admin.action(description="Mark selected shops as VISIBLE (View)")
    def mark_visible(self, request, queryset):
        updated = queryset.update(is_visible=True)
        self.message_user(request, f"{updated} shop(s) set to visible.")

    @admin.action(description="Mark selected shops as HIDDEN (Hide)")
    def mark_hidden(self, request, queryset):
        updated = queryset.update(is_visible=False)
        self.message_user(request, f"{updated} shop(s) set to hidden.")

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom = [
            path(
                "<path:object_id>/toggle-visibility/",
                self.admin_site.admin_view(self.toggle_visibility),
                name="businesswebinfo_toggle_visibility",
            ),
        ]
        return custom + urls

    def toggle_visibility(self, request, object_id):
        from django.contrib import messages
        from django.shortcuts import redirect

        if request.method != "POST":
            return HttpResponseNotAllowed(["POST"])

        obj = self.get_object(request, object_id)
        if obj is None:
            messages.error(request, "Shop not found.")
            return redirect("admin:mainapp_businesswebinfo_changelist")
        obj.is_visible = not obj.is_visible
        obj.save(update_fields=["is_visible"])
        state = "visible" if obj.is_visible else "hidden"
        messages.success(request, f"“{obj.bname}” is now {state}.")
        return redirect("admin:mainapp_businesswebinfo_changelist")
