import random

from django.shortcuts import render, redirect
from django.contrib.auth import logout

from ..models import Homeimgs, ProductCategory
from ..product_catalog import get_product_model
from ._shared import randomSample


def _featured_category_cards():
    """
    One card per active catalog category, with a random project from that
    category's dedicated product table.

    Skip placeholder promo images: any mainimgbasetxt containing 'promoimg.png'
    is excluded so the homepage only features real project photos.
    """
    cards = []
    categories = ProductCategory.objects.filter(is_active=True).order_by(
        "sort_order", "name"
    )
    for cat in categories:
        Model = get_product_model(cat.slug)
        product = None
        if Model is not None:
            qs = (
                Model.objects.all()
                .only(
                    "prodid",
                    "productname",
                    "highlighttitle",
                    "mainimgbasetxt",
                )
                .exclude(mainimgbasetxt__icontains="promoimg.png")
            )
            # Prefer projects that have a real non-promo image
            with_img = qs.exclude(mainimgbasetxt__in=["", "*"])
            pool = list(with_img.values_list("prodid", flat=True))
            # Do not fall back to promo-only / missing-image rows for featured
            if pool:
                product = Model.objects.filter(prodid=random.choice(pool)).first()
        cards.append({"category": cat, "product": product})
    return cards


def welcome(request):
    return render(
        request,
        "systemsetup/welcome.html",
        {"featured_category_cards": _featured_category_cards()},
    )


def dashboard(request):
    home_images = randomSample(Homeimgs.public_qs(), limit=10)
    return render(request, "systemsetup/herosection.html", {"home_images": home_images})


def gallery(request):
    galleryImgs = randomSample(Homeimgs.public_qs())
    return render(request, "systemsetup/gallery.html", {"galleryImgs": galleryImgs})


def contactus(request):
    return render(request, "systemsetup/contactus.html")


def aboutus(request):
    return render(request, "systemsetup/aboutus.html")


def logoutView(request):
    logout(request)
    return redirect("/")
