from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import *
from .models import Comment


@receiver(post_save, sender=Comment)
def new_reply_signal(instance, created, **kwargs):
    if created:
        reply_id = Comment.objects.get(id=instance.id).id
        new_comment_email_task.delay(reply_id)

