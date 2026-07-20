import logging

from django.db import Error as DjangoDbError
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from ..models import AccessoriesProd
from ._shared import paginate

logger = logging.getLogger(__name__)

ACCESSORIES_PER_PAGE = 24


def accessoriesProjects(request):
    try:
        accessProd = AccessoriesProd.objects.all().order_by('-timestamp')
        page_obj, base_qs = paginate(request, accessProd, ACCESSORIES_PER_PAGE)
        return render(request, 'AccessoriesSection/accessprodlist.html', {'accessProd': page_obj, 'page_obj': page_obj, 'base_qs': base_qs})
    except DjangoDbError as error:
        logger.warning("Database error in accessoriesProjects: %s", error)
        return render(request, 'AccessoriesSection/accessprodlist.html', {'accessProd': [], 'error': "Accessories are temporarily unavailable. Please try again shortly."}, status=500)
    except Exception:
        logger.exception("Unexpected error in accessoriesProjects")
        return render(request, 'AccessoriesSection/accessprodlist.html', {'accessProd': [], 'error': "Something went wrong loading accessories."}, status=500)


def accessoriesView(request, apid):
    try:
        accessProd = get_object_or_404(AccessoriesProd, apid=apid)
        return render(request, 'AccessoriesSection/accessprodview.html', {'accessProd': accessProd})
    except Http404:
        raise
    except DjangoDbError as error:
        logger.warning("Database error in accessoriesView(%s): %s", apid, error)
        return render(request, 'AccessoriesSection/accessprodview.html', {'error': "This item is temporarily unavailable. Please try again shortly."}, status=500)
    except Exception:
        logger.exception("Unexpected error in accessoriesView(%s)", apid)
        return render(request, 'AccessoriesSection/accessprodview.html', {'error': "Something went wrong loading this item."}, status=500)
