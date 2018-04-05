import datetime
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse

from blog.models import Post


def index(request):
    post = Post.objects.latest('created_at')
    return render(request, 'index.html', {
        'started_coding_date': datetime.datetime(2004, 4, 8),
        'post': post
    })

def contact(request):
    return render(request, 'contact.html', {})
