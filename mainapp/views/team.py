from django.shortcuts import render

from ..models import TeamMember


def our_team(request):
    team_members = TeamMember.objects.all().order_by('timestamp')
    return render(request, 'TeamSection/ourteam.html', {'team_members': team_members})


def team_member_profile(request):
    name = request.GET.get('name')
    member = None
    if name:
        try:
            member = TeamMember.objects.get(name__iexact=name)
        except TeamMember.DoesNotExist:
            member = None
        except TeamMember.MultipleObjectsReturned:
            member = TeamMember.objects.filter(name__iexact=name).order_by('timestamp').first()
    if not member:
        return render(
            request,
            'TeamSection/ourteam_profile.html',
            {'member': None, 'error': 'Team member not found.'},
            status=404,
        )
    return render(request, 'TeamSection/ourteam_profile.html', {'member': member})
