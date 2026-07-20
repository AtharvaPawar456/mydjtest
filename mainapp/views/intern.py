from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import InternDetails, InternOpportunity
from ._shared import isAjaxRequest, paginate

INTERNS_PER_PAGE = 20


def internship_listing(request):
    interns = InternDetails.objects.all().order_by('-timestamp')
    stipend_filter = request.GET.get('stipend', 'all').strip().lower()
    if stipend_filter in ('yes', 'stipend', 'paid', '1', 'true'):
        interns = interns.filter(is_stipend=True)
        stipend_filter = 'stipend'
    elif stipend_filter in ('no', 'unstipend', 'unpaid', '0', 'false'):
        interns = interns.filter(is_stipend=False)
        stipend_filter = 'unstipend'
    else:
        stipend_filter = 'all'

    # One aggregate query instead of 4 separate COUNT(*) queries; total is
    # always stipend_count + unstipend_count since is_stipend is a boolean partition.
    counts = InternDetails.objects.aggregate(
        stipend_count=Count('internid', filter=Q(is_stipend=True)),
        unstipend_count=Count('internid', filter=Q(is_stipend=False)),
    )
    stipend_count = counts['stipend_count']
    unstipend_count = counts['unstipend_count']
    total_intern_count = stipend_count + unstipend_count
    intern_count = stipend_count if stipend_filter == 'stipend' else (
        unstipend_count if stipend_filter == 'unstipend' else total_intern_count
    )

    # Only load the columns the list-card template renders.
    interns = interns.only('internid', 'name', 'role', 'experience', 'photo_base64', 'is_stipend')

    page_obj, base_qs = paginate(request, interns, INTERNS_PER_PAGE)

    content = {
        'interns': page_obj,
        'page_obj': page_obj,
        'base_qs': base_qs,
        'intern_count': intern_count,
        'stipend_filter': stipend_filter,
        'stipend_count': stipend_count,
        'unstipend_count': unstipend_count,
        'total_intern_count': total_intern_count,
    }
    template = 'InternSection/_intern_results.html' if isAjaxRequest(request) else 'InternSection/internship_listing.html'
    return render(request, template, content)


def intern_profile(request, intern_id):
    intern = get_object_or_404(InternDetails, internid=intern_id)
    return render(request, 'InternSection/intern_profile.html', {'intern': intern})


def internship_opportunities(request):
    # Public page: only rows marked visible (| in intern-ops.txt / is_visible=True).
    all_ops = InternOpportunity.objects.filter(is_visible=True).order_by('opid')
    track = request.GET.get('track', '').strip()
    stipend_raw = request.GET.get('stipend', 'all').strip().lower()

    if stipend_raw in ('yes', 'stipend', 'paid', '1', 'true'):
        stipend_filter = 'stipend'
    elif stipend_raw in ('no', 'unstipend', 'unpaid', '0', 'false'):
        stipend_filter = 'unstipend'
    else:
        stipend_filter = 'all'

    opportunities = all_ops
    if track:
        opportunities = opportunities.filter(track__iexact=track)
    if stipend_filter == 'stipend':
        opportunities = opportunities.filter(is_stipend=True)
    elif stipend_filter == 'unstipend':
        opportunities = opportunities.filter(is_stipend=False)

    counts = all_ops.aggregate(
        stipend_count=Count('opid', filter=Q(is_stipend=True)),
        unstipend_count=Count('opid', filter=Q(is_stipend=False)),
    )
    tracks = sorted(
        all_ops.exclude(track='').values_list('track', flat=True).distinct()
    )

    content = {
        'opportunities': opportunities,
        'opportunity_count': opportunities.count(),
        'total_opportunity_count': all_ops.count(),
        'tracks': tracks,
        'active_track': track,
        'stipend_filter': stipend_filter,
        'stipend_count': counts['stipend_count'],
        'unstipend_count': counts['unstipend_count'],
        'apply_drive_url': 'https://drive.google.com/drive/folders/1Hq8g1WI-PK7E6ASr4tIRei2Xd8Rt4mim?usp=sharing',
    }
    template = 'InternSection/_opportunity_results.html' if isAjaxRequest(request) else 'InternSection/internship_opportunities.html'
    return render(request, template, content)
