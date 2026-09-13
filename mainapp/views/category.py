from django.shortcuts import render


def kids_projects(request):
    return render(request, 'projectscategory/kids_projects.html')


def engineering_projects_category(request):
    return render(request, 'projectscategory/engineering_projects_category.html')
