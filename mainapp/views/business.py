import logging

from django.db import Error as DjangoDbError
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from ..models import Businesswebinfo
from ._shared import paginate

logger = logging.getLogger(__name__)

SHOPS_PER_PAGE = 24


def viewAllShop(request):
    """
    io: request
    work: lists all shops in card layout with SEO-friendly content
    """
    try:
        shopList = Businesswebinfo.objects.filter(is_visible=True).order_by('-btimestamp')
        shopCount = shopList.count()
        page_obj, base_qs = paginate(request, shopList, SHOPS_PER_PAGE)

        content = {
            "shopList": page_obj,
            "page_obj": page_obj,
            "base_qs": base_qs,
            "shopCount": shopCount,
        }
        return render(request, "BusinessSection/allshops.html", content)

    except DjangoDbError as error:
        logger.warning("Database error in viewAllShop: %s", error)
        return render(
            request,
            "BusinessSection/allshops.html",
            {"error": "The shop directory is temporarily unavailable. Please try again shortly."},
            status=500,
        )
    except Exception:
        logger.exception("Unexpected error in viewAllShop")
        return render(
            request,
            "BusinessSection/allshops.html",
            {"error": "Something went wrong loading the shop directory."},
            status=500,
        )


def viewShop(request, shopname):
    """
    io: request, shopname (str)
    work: fetches shop details from DB using URL name and renders professional profile page
    """
    try:
        shop = get_object_or_404(Businesswebinfo, bname__iexact=shopname, is_visible=True)

        def _split_media(value):
            if not value or value.strip() == "*":
                return []
            items = []
            for part in value.replace("\r", "\n").split(";"):
                for chunk in part.split("\n"):
                    url = chunk.strip()
                    if url and url != "*":
                        # Normalize GitHub raw -> jsDelivr for more reliable browser loading
                        raw_prefix = "https://raw.githubusercontent.com/AtharvaPawar456/hmp_assets/refs/heads/main/"
                        raw_prefix2 = "https://raw.githubusercontent.com/AtharvaPawar456/hmp_assets/main/"
                        if url.startswith(raw_prefix):
                            url = "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/" + url[len(raw_prefix):]
                        elif url.startswith(raw_prefix2):
                            url = "https://cdn.jsdelivr.net/gh/AtharvaPawar456/hmp_assets@main/" + url[len(raw_prefix2):]
                        items.append(url)
            return items

        galleryImages = _split_media(shop.bgallery)
        ownerImages = _split_media(shop.bownerimgs)
        ytLinks = _split_media(shop.bytlinks)
        webLinks = _split_media(shop.bweblinks)

        # Also normalize main image for the template
        main_imgs = _split_media(shop.bmainimg)
        if main_imgs:
            shop.bmainimg = main_imgs[0]

        seoKeywords = ", ".join(
            set(
                word.lower()
                for word in f"{shop.bname} {shop.bcat} {shop.btags} {shop.bhighlight}".replace(",", " ").split()
                if len(word) > 3
            )
        )

        content = {
            "shop": shop,
            "galleryImages": galleryImages,
            "ownerImages": ownerImages,
            "ytLinks": ytLinks,
            "webLinks": webLinks,
            "seoKeywords": seoKeywords,
        }

        return render(request, "BusinessSection/shop.html", content)

    except Http404:
        raise
    except DjangoDbError as error:
        logger.warning("Database error in viewShop(%s): %s", shopname, error)
        return render(
            request,
            "BusinessSection/shop.html",
            {"error": "This shop page is temporarily unavailable. Please try again shortly.", "shop": None},
            status=500,
        )
    except Exception:
        logger.exception("Unexpected error in viewShop(%s)", shopname)
        return render(
            request,
            "BusinessSection/shop.html",
            {"error": "Something went wrong loading this shop.", "shop": None},
            status=500,
        )
