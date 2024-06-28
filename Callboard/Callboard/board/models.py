from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from .extensions import *


class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    content = RichTextUploadingField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.text}'

    def get_absolute_url(self):
        return reverse('posts-detail', args=[str(self.id)])


class Comment(models.Model):
    comment_post = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    active =models.BooleanField(default=False)
