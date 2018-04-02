import datetime
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html', {
        'started_coding_date': datetime.datetime(2004, 4, 8)
    })

def contact(request):
    return render(request, 'contact.html', {})
