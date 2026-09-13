from django.shortcuts import render


def privacy_policy(request):
    return render(request, 'systemsetup/privacy_policy.html')


def terms_of_service(request):
    return render(request, 'systemsetup/terms_of_service.html')
