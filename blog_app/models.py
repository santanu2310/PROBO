from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone
from tinymce.models import HTMLField
# Create your models here.

class Subscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='site_dynamic')
    url = models.SlugField(max_length=400, unique=True, blank=True)

    def __str__(self):
        return self.name


class Tags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Writer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_pic = models.ImageField(upload_to='site_dynamic')
    name = models.CharField(max_length=100)
    short_desc = models.CharField(max_length=30)
    insta = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    twiter = models.CharField(max_length=100, blank=True, null=True)
    youtube = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    tags = models.ManyToManyField(Tags, blank=True)
    url = models.SlugField(max_length=400, unique=True, blank=True)
    cover_image = models.ImageField(upload_to = 'blog_image')
    banner = models.ImageField(upload_to='blog_image')
    eidtors_pick = models.BooleanField(default = False)
    visitors = models.IntegerField(default=0,editable=False)
    short_desc = models.CharField(max_length=500)
    aritcle = HTMLField(blank=True,default="")
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name
    
    def context_to_dict(self):
        return {
            "name": self.name,
            "url": f'http://127.0.0.1:8000/article/{self.id}',
            "short_desc": self.short_desc,
            "author": self.writer.name,
        }
