from django.db import models
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    title   = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.title


class Post(models.Model):
    title   = models.CharField(max_length=200, default='')
    slug    = models.SlugField(unique=True, default='')
    description = models.TextField(default='')
    content = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)
