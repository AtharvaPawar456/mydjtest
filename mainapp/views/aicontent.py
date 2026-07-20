import logging

from django.db import Error as DjangoDbError
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from ..models import AicontentProd
from ._shared import paginate

logger = logging.getLogger(__name__)

AICONTENT_PER_PAGE = 24


def aicontentList(request):
    try:
        aiContent = AicontentProd.objects.all().order_by('-timestamp')
        page_obj, base_qs = paginate(request, aiContent, AICONTENT_PER_PAGE)
        return render(request, 'AiContentSection/aicontentlist.html', {'aiContent': page_obj, 'page_obj': page_obj, 'base_qs': base_qs})
    except DjangoDbError as error:
        logger.warning("Database error in aicontentList: %s", error)
        return render(request, 'AiContentSection/aicontentlist.html', {'aiContent': [], 'error': "AI content is temporarily unavailable. Please try again shortly."}, status=500)
    except Exception:
        logger.exception("Unexpected error in aicontentList")
        return render(request, 'AiContentSection/aicontentlist.html', {'aiContent': [], 'error': "Something went wrong loading AI content."}, status=500)


def aicontentView(request, aiid):
    try:
        aiContent = get_object_or_404(AicontentProd, aiid=aiid)
        return render(request, 'AiContentSection/aicontentview.html', {'aiContent': aiContent})
    except Http404:
        raise
    except DjangoDbError as error:
        logger.warning("Database error in aicontentView(%s): %s", aiid, error)
        return render(request, 'AiContentSection/aicontentview.html', {'error': "This item is temporarily unavailable. Please try again shortly."}, status=500)
    except Exception:
        logger.exception("Unexpected error in aicontentView(%s)", aiid)
        return render(request, 'AiContentSection/aicontentview.html', {'error': "Something went wrong loading this item."}, status=500)
