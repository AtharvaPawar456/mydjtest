import logging

from django.db import Error as DjangoDbError
from django.shortcuts import render, redirect
from django.http import Http404
from ..models import ProductCategory
from ..product_categories_data import canonical_slug
from ..product_catalog import (
    get_product_model,
    get_product_or_404,
    find_product_by_id,
    list_products,
)
from ._shared import isAjaxRequest, paginate

logger = logging.getLogger(__name__)

PRODUCTS_PER_PAGE = 24


def resolve_category(value: str):
    """Resolve ?productcat= to a ProductCategory row (canonical or legacy slug)."""
    raw = (value or "").strip()
    if not raw:
        return None
    slug = canonical_slug(raw)
    cat = ProductCategory.objects.filter(is_active=True, slug__iexact=slug).first()
    if cat:
        return cat
    for c in ProductCategory.objects.filter(is_active=True):
        if c.matches_query(raw) or c.matches_query(slug):
            return c
    return None


def getQuickFilters(category_slug_or_obj):
    """Hashtag sub-filters from ProductCategory.hashtags."""
    try:
        if not category_slug_or_obj:
            return []
        if isinstance(category_slug_or_obj, ProductCategory):
            return category_slug_or_obj.hashtag_list
        cat = resolve_category(str(category_slug_or_obj))
        return cat.hashtag_list if cat else []
    except Exception as error:
        print("Quick filter error:", error)
        return []


def productlist(request):
    try:
        category_raw = request.GET.get("productcat", "").strip()
        searchQuery = request.GET.get("q", "").strip()

        active_category = resolve_category(category_raw)
        category = (
            active_category.slug
            if active_category
            else (canonical_slug(category_raw) if category_raw else "")
        )

        # Unknown slug that doesn't map to a model → empty list
        if category and get_product_model(category) is None and not active_category:
            products = []
        else:
            products = list_products(
                category_slug=category or None,
                search_query=searchQuery,
            )

        productListcount = len(products)
        page_obj, base_qs = paginate(request, products, PRODUCTS_PER_PAGE)
        quickFilters = getQuickFilters(active_category or category)

        content = {
            "productList": page_obj,
            "page_obj": page_obj,
            "base_qs": base_qs,
            "productListcount": productListcount,
            "searchQuery": searchQuery,
            "quickFilters": quickFilters,
            "active_productcat": category,
            "category_display_name": (
                active_category.name if active_category else (category or "")
            ),
            "catalog_categories": ProductCategory.objects.filter(is_active=True),
        }

        template = (
            "ProductSection/_product_results.html"
            if isAjaxRequest(request)
            else "ProductSection/productlist.html"
        )
        return render(request, template, content)

    except DjangoDbError as error:
        logger.warning("Database error in productlist: %s", error)
        return render(
            request,
            "ProductSection/productlist.html",
            {"error": "The catalog is temporarily unavailable. Please try again shortly."},
            status=500,
        )
    except Exception:
        logger.exception("Unexpected error in productlist")
        return render(
            request,
            "ProductSection/productlist.html",
            {"error": "Something went wrong loading the catalog."},
            status=500,
        )


def productinfo(request, prod_id, category_slug=None):
    try:
        if category_slug:
            product = get_product_or_404(category_slug, prod_id)
        else:
            # Legacy URL /productinfo/<id>/ — resolve across category tables
            product = find_product_by_id(prod_id)
            if product is None:
                raise Http404("Product not found")
            # Canonical redirect to category-scoped URL
            return redirect(
                "productinfo",
                category_slug=product.category_slug,
                prod_id=product.prodid,
                permanent=False,
            )

        seoKeywords = set()

        def extractKeywords(text):
            if not text:
                return []
            return [
                word.lower()
                for word in text.replace(",", " ").replace(".", " ").split()
                if len(word) > 3
            ]

        nogallery = product.gallery == "*"
        productImages = [img for img in product.gallery.split(";") if img]
        productYTlinks = [link for link in product.ytlinks.split(";") if link]

        seoKeywords.update(extractKeywords(product.productname))
        seoKeywords.update(extractKeywords(product.highlighttitle))
        seoKeywords.update(extractKeywords(product.prodinfo))
        if product.category_label:
            seoKeywords.add(product.category_label.lower())

        seoKeywords.update(
            [
                "engineering project",
                "iot project",
                "final year project",
                "student project",
                "diy project",
                "real world project",
                "learning project",
                "hands on project",
            ]
        )

        content = {
            "product": product,
            "nogallery": nogallery,
            "productImages": productImages,
            "productYTlinks": productYTlinks,
            "seoKeywords": ", ".join(sorted(seoKeywords)),
            "product_category_slug": product.category_slug,
        }
        return render(request, "ProductSection/productinfo.html", content)

    except Http404:
        raise
    except DjangoDbError as error:
        logger.warning("Database error in productinfo(%s): %s", prod_id, error)
        return render(
            request,
            "ProductSection/productinfo.html",
            {
                "error": "This project is temporarily unavailable. Please try again shortly."
            },
            status=500,
        )
    except Exception:
        logger.exception("Unexpected error in productinfo(%s)", prod_id)
        return render(
            request,
            "ProductSection/productinfo.html",
            {"error": "Something went wrong loading this project."},
            status=500,
        )
