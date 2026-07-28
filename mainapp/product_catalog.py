"""
Catalog helpers for the six per-category project models.

Use this instead of querying a single mixed ProductInfo table.
"""
from __future__ import annotations

from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import (
    Project_Craft,
    Project_Hardware,
    Project_Mechanical,
    Project_Science,
    Project_Simulation,
    Project_Software,
)
from .product_categories_data import canonical_slug

# slug → concrete model
CATEGORY_PRODUCT_MODELS = {
    Project_Software.category_slug: Project_Software,
    Project_Hardware.category_slug: Project_Hardware,
    Project_Mechanical.category_slug: Project_Mechanical,
    Project_Simulation.category_slug: Project_Simulation,
    Project_Science.category_slug: Project_Science,
    Project_Craft.category_slug: Project_Craft,
}

ALL_PRODUCT_MODELS = list(CATEGORY_PRODUCT_MODELS.values())

PRODUCT_FIELD_NAMES = (
    "prodid",
    "productname",
    "mainimgbasetxt",
    "prodtags",
    "prodcost",
    "highlighttitle",
    "prodinfo",
    "gallery",
    "ytlinks",
    "components",
    "documents",
    "timestamp",
)


def get_product_model(slug: str):
    """Return the product model class for a category slug (or legacy alias)."""
    key = canonical_slug(slug)
    return CATEGORY_PRODUCT_MODELS.get(key)


def get_product(category_slug: str, prod_id: int):
    Model = get_product_model(category_slug)
    if Model is None:
        return None
    return Model.objects.filter(prodid=prod_id).first()


def get_product_or_404(category_slug: str, prod_id: int):
    Model = get_product_model(category_slug)
    if Model is None:
        from django.http import Http404

        raise Http404("Unknown product category")
    return get_object_or_404(Model, prodid=prod_id)


def find_product_by_id(prod_id: int):
    """
    Locate a product by primary key across all category tables.
    Safe because IDs were migrated from a single shared ProductInfo sequence
    (at most one table holds a given prodid).
    """
    for Model in ALL_PRODUCT_MODELS:
        obj = Model.objects.filter(prodid=prod_id).first()
        if obj is not None:
            return obj
    return None


def search_filter_q(search_query: str) -> Q:
    return (
        Q(productname__icontains=search_query)
        | Q(prodtags__icontains=search_query)
        | Q(highlighttitle__icontains=search_query)
        | Q(prodinfo__icontains=search_query)
    )


def list_products(*, category_slug: str | None = None, search_query: str = ""):
    """
    Return a list of product instances sorted by timestamp desc.
    Suitable for catalogs of this site's size; paginate in the view.
    """
    models = []
    if category_slug:
        Model = get_product_model(category_slug)
        if Model is not None:
            models = [Model]
    else:
        models = ALL_PRODUCT_MODELS

    items = []
    for Model in models:
        qs = Model.objects.all()
        if search_query:
            qs = qs.filter(search_filter_q(search_query))
        items.extend(list(qs))
    items.sort(key=lambda p: p.timestamp or p.prodid, reverse=True)
    return items


def count_products(*, category_slug: str | None = None) -> int:
    if category_slug:
        Model = get_product_model(category_slug)
        return Model.objects.count() if Model else 0
    return sum(M.objects.count() for M in ALL_PRODUCT_MODELS)


def product_row_dict(obj) -> dict:
    """Serialize a product instance to a plain dict (for migrations / seeds)."""
    return {name: getattr(obj, name) for name in PRODUCT_FIELD_NAMES}
