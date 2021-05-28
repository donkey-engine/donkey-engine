from smtplib import SMTPException

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.helpers.email import send_email_confirmation


@receiver(post_save, sender=User)
def handle_user_post_save(sender, instance, created, **kwargs):
    if created:
        try:
            send_email_confirmation(instance)
        except SMTPException:
            instance.is_active = True
            instance.save()
