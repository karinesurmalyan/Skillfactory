from celery import shared_task
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import *


import time
import datetime


@shared_task
def new_comment_email_task(reply_id):
    comment = Comment.objects.get(id=reply_id)
    post = comment.comment_post

    message = render_to_string(
        'new_comment_email.html',
        {
            'post_author': post.author.username,
            'comment_author': comment.comment_author,
            'post_title': post.title,
            'comment_text': comment.text[:20] + '...',
        }
    )
    email = EmailMessage(
        subject='Новый отклик!',
        body=message,
        to=[post.author.email]
    )

    email.send()


@shared_task
def status_upd_email_task(reply_id):
    comment = Comment.objects.get(id=reply_id)
    post = comment.comment_post

    message = render_to_string(
        'status_upd_email.html',
        {
            'comment_author': comment.comment_author.username,
            'post_title': post.title
        }
    )
    email = EmailMessage(
        subject='Статус изменен!',
        body=message,
        to=[comment.comment_author.email]
    )
    email.send()


@shared_task
def weekly_mailing_task():
    today = datetime.datetime.now()
    week_ago = today - datetime.timedelta(days=7)
    posts = Announcement.objects.filter(pub_date__gte=week_ago)
    recipients = User.objects.values_list('email', flat=True)

    message = render_to_string(
        'weekly_mailing.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    email = EmailMultiAlternatives(
        subject='Новые объявления',
        body='',
        to=recipients
    )
    email.attach_alternative(message, 'text/html')
    email.send()