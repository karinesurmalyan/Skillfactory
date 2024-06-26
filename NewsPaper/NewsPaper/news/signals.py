from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives
from .models import PostCategory
from django.template.loader import render_to_string
from .tasks import notification_of_new_post

from django.conf import settings


# def send_notifications(preview, pk, title, subscribers):
#     for s in subscribers:
#         sub_name = s.username
#         sub_email = [s.email]
#         html_contect = render_to_string(
#             'new_post_email.html',
#             {
#                 'text': preview,
#                 'link': f'{settings.SITE_URL}/news/{pk}',
#                 'sub_name': sub_name
#             }
#         )
#
#         msg = EmailMultiAlternatives(
#             subject=title,
#             body='',
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=sub_email
#         )
#
#         msg.attach_alternative(html_contect, 'text/html')
#         msg.send()
#

@receiver(m2m_changed, sender=PostCategory)
def new_post_notification(sender, instance, **kwargs):
    if kwargs['action'] == 'post__add':
        notification_of_new_post.delay(instance.pk)
        # categories = instance.category.all()
        # subscribers_emails = []
        #
        # for cat in categories:
        #     subscribers = cat.subscribers.all()
        #     subscribers_emails += [s.email for s in subscribers]
