from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from .extensions import *


class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)


class Announcement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    content = RichTextUploadingField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=ROLES, default=None)

    def __str__(self):
        return f'{self.title} {self.text}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Comment(models.Model):
    comment_post = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    ia_accepted = models.BooleanField(default=False)
