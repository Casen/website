from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse

from .models import Post

def index(request):
    post = Post.objects.latest('created_at')
    template = loader.get_template('blog/index.html')
    context = {
        'post': post
    }
    return HttpResponse(template.render(context, request)) 

def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    template = loader.get_template('blog/detail.html')
    context = {
        'post': post
    }
    return HttpResponse(template.render(context, request)) 
