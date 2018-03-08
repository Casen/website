from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse

from .models import Project

def index(request):
    all_projects = Project.objects.all();
    return render(request, 'projects/index.html', {"projects": all_projects})

def detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'projects/detail.html', {"project": project})
