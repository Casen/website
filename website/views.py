from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html', {})
