"""Small helpers for building minimal valid model instances in tests."""
from django.contrib.auth.models import User

from ..models import (
    TeamMember,
    InternDetails,
    Businesswebinfo,
    AccessoriesProd,
    AicontentProd,
    EarnTask,
    Homeimgs,
    YTvideos,
    Contactus,
    ProductCategory,
)
from ..product_catalog import get_product_model


def make_category(**overrides):
    defaults = {
        "name": "Hardware",
        "slug": "hardware",
        "legacy_slugs": "hardwareprojects",
        "hashtags": "iot, esp32, arduino",
        "sort_order": 20,
        "is_active": True,
    }
    defaults.update(overrides)
    obj, _ = ProductCategory.objects.get_or_create(
        slug=defaults["slug"], defaults=defaults
    )
    return obj


def make_product(**overrides):
    """Create a product in the appropriate category table (default: hardware)."""
    slug = overrides.pop("category_slug", None)
    productcat = overrides.pop("productcat", None)
    if slug is None:
        slug = productcat or "hardware"
    from ..product_categories_data import canonical_slug

    slug = canonical_slug(slug)
    Model = get_product_model(slug)
    if Model is None:
        raise ValueError(f"Unknown product category slug: {slug}")
    # ensure category row exists for filters
    make_category(
        name=Model.category_name,
        slug=Model.category_slug,
        sort_order=10,
    )
    defaults = {
        "productname": "Smart Test Widget",
        "mainimgbasetxt": "https://example.com/widget.jpg",
        "prodtags": "esp32, test",
        "prodcost": "15000",
        "highlighttitle": "A test widget",
        "prodinfo": "<p>Test info</p>",
        "gallery": "*",
        "ytlinks": "*",
    }
    defaults.update(overrides)
    return Model.objects.create(**defaults)


def make_team_member(**overrides):
    defaults = {"name": "Test Member", "role": "Engineer", "experience": "5 years"}
    defaults.update(overrides)
    return TeamMember.objects.create(**defaults)


def make_intern(**overrides):
    defaults = {
        "name": "Test Intern",
        "role": "Intern",
        "experience": "1 year",
        "is_stipend": True,
    }
    defaults.update(overrides)
    return InternDetails.objects.create(**defaults)


def make_shop(**overrides):
    defaults = {
        "bname": "Test-Shop",
        "bcat": "Electronics",
        "bmainimg": "https://example.com/shop.jpg",
        "is_visible": True,
    }
    defaults.update(overrides)
    return Businesswebinfo.objects.create(**defaults)


def make_accessory(**overrides):
    defaults = {
        "aptitle": "Test Accessory",
        "apsale": "500",
        "apprice": "700",
        "apimglink": "https://example.com/a.jpg",
    }
    defaults.update(overrides)
    return AccessoriesProd.objects.create(**defaults)


def make_aicontent(**overrides):
    defaults = {
        "aititle": "Test AI Content",
        "aisale": "300",
        "aiprice": "400",
        "aiimglink": "https://example.com/ai.jpg",
    }
    defaults.update(overrides)
    return AicontentProd.objects.create(**defaults)


def make_earn_task(**overrides):
    defaults = {
        "etitle": "Test Task",
        "eamount": "1000",
        "estatus": "active",
        "eimglink": "https://example.com/t.jpg",
    }
    defaults.update(overrides)
    return EarnTask.objects.create(**defaults)


def make_home_image(**overrides):
    defaults = {
        "imgtitle": "Test Image",
        "imglink": "https://example.com/home.jpg",
    }
    defaults.update(overrides)
    return Homeimgs.objects.create(**defaults)


def make_video(**overrides):
    defaults = {
        "videotitle": "Test Video",
        "videolink": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    }
    defaults.update(overrides)
    return YTvideos.objects.create(**defaults)


def make_contact_message(**overrides):
    defaults = {
        "name": "Tester",
        "emailid": "tester@example.com",
        "msg": "Hello",
    }
    defaults.update(overrides)
    return Contactus.objects.create(**defaults)


def make_admin_user(username="atharva", password="test-pass-123"):
    return User.objects.create_superuser(
        username=username, email="admin@example.com", password=password
    )
