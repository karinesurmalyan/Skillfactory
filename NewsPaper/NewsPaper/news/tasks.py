import datetime
from celery import shared_task
from celery.schedules import crontab
from .models import Post, Category
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string


@shared_task
def notification_of_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    subscribers_list = []

    for c in categories:
        subscribers = c.subscribers.all()
        subscribers_list += [s for s in subscribers]

    for s in subscribers_list:
        sub_name = s.username
        sub_email = [s.email]
        html_content = render_to_string(
            'new_post_email.html',
            {
                'text': post.preview(),
                'link': f'{settings.SITE_URL}/news/{pk}',
                'sub_name': sub_name
            }
        )
        msg = EmailMultiAlternatives(
            subject=post.title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=sub_email
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def weekly_mail():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_in__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', 'subscribers__username'))
    for s in subscribers:
        sub_name = s[1]
        sub_email = [s[0]]
        html_content = render_to_string(
            'weekly_email.html',
            {
                'link': settings.SITE_URL,
                'posts': posts,
                'sub_name': sub_name
            }
        )

        msg = EmailMultiAlternatives(
            subject='Недельная рассылка',
            body='',
            from_emil=settings.DEFAULT_FROM_EMAIL,
            to=sub_email,
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()