from django.db import models
from django.utils.text import slugify

# Create your models here.

class Post(models.Model):
    title   = models.CharField(max_length=200, default='')
    slug    = models.SlugField(unique=True, default='')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)
