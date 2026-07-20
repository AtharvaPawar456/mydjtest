from django.db.models import Q
from django.shortcuts import render

from ..models import (
    InternDetails,
    Businesswebinfo,
    TeamMember,
    AccessoriesProd,
    AicontentProd,
)
from ..product_catalog import ALL_PRODUCT_MODELS


def global_search(request):
    """
    Searches across products (all category tables), interns, shops, team,
    accessories and AI content.
    """
    q = request.GET.get("q", "").strip()

    results = {
        "products": [],
        "interns": [],
        "shops": [],
        "team": [],
        "accessories": [],
        "aicontent": [],
    }

    if q:
        products = []
        for Model in ALL_PRODUCT_MODELS:
            products.extend(
                list(
                    Model.objects.filter(
                        Q(productname__icontains=q)
                        | Q(prodtags__icontains=q)
                        | Q(highlighttitle__icontains=q)
                    ).only("prodid", "productname", "mainimgbasetxt")[:12]
                )
            )
        products.sort(key=lambda p: p.timestamp, reverse=True)
        results["products"] = products[:12]

        results["interns"] = InternDetails.objects.filter(
            Q(name__icontains=q) | Q(role__icontains=q)
        ).only("internid", "name", "role", "photo_base64")[:12]

        results["shops"] = Businesswebinfo.objects.filter(
            Q(bname__icontains=q) | Q(bcat__icontains=q) | Q(btags__icontains=q),
            is_visible=True,
        ).only("bname", "bcat", "bmainimg")[:12]

        results["team"] = TeamMember.objects.filter(
            Q(name__icontains=q) | Q(role__icontains=q)
        ).only("devid", "name", "role", "photo_base64")[:12]

        results["accessories"] = AccessoriesProd.objects.filter(
            Q(aptitle__icontains=q) | Q(aptag__icontains=q)
        ).only("apid", "aptitle", "apimglink")[:12]

        results["aicontent"] = AicontentProd.objects.filter(
            Q(aititle__icontains=q) | Q(aitag__icontains=q)
        ).only("aiid", "aititle", "aiimglink")[:12]

    total_count = sum(len(v) for v in results.values())

    return render(
        request,
        "systemsetup/search_results.html",
        {
            "query": q,
            "results": results,
            "total_count": total_count,
        },
    )
