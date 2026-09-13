"""Helpers shared across the view modules in this package."""
import random

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from PIL import Image, UnidentifiedImageError

MAX_UPLOAD_IMAGE_BYTES = 5 * 1024 * 1024  # 5MB


def validateUploadedImage(photo):
    """
    Validates an uploaded photo is a decodable image under the size limit.
    Raises ValidationError if invalid; leaves the file pointer reset to 0 either way.
    """
    try:
        if photo.size > MAX_UPLOAD_IMAGE_BYTES:
            raise ValidationError(
                f"Image must be smaller than {MAX_UPLOAD_IMAGE_BYTES // (1024 * 1024)}MB."
            )
        try:
            Image.open(photo).verify()
        except UnidentifiedImageError:
            raise ValidationError("Uploaded file is not a valid image.")
    finally:
        photo.seek(0)


def isAjaxRequest(request):
    """
    True for fetch() calls made by mainapp/static/mainapp/js/ajax-filters.js,
    which sets this header to ask for a results-only partial instead of a full page.
    """
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


def paginate(request, queryset, per_page):
    """
    Paginates a queryset/list using the `page` GET param. Returns
    (page_obj, base_querystring) where base_querystring is the current
    query string with `page` stripped, ready for `?{{ base_qs }}&page=N`
    links that preserve existing filters (category, search, stipend, etc.).
    """
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(request.GET.get('page'))
    base_qs = request.GET.copy()
    base_qs.pop('page', None)
    return page_obj, base_qs.urlencode()


def randomSample(queryset, limit=None):
    """
    Returns rows from queryset in random order without relying on order_by('?'),
    which forces the database to compute a random value per row and sort the
    whole table on every call. Samples primary keys in Python instead.
    """
    ids = list(queryset.values_list('pk', flat=True))
    random.shuffle(ids)
    if limit is not None:
        ids = ids[:limit]
    objectsById = queryset.model.objects.in_bulk(ids)
    return [objectsById[pk] for pk in ids if pk in objectsById]
