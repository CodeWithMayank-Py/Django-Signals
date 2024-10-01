from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.dispatch import receiver
from .models import Post

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """Send an email when a new user is created"""
    if created:
        send_mail(
            subject="Welcome to our site!",
            message='Thank you for registering, {}!'.format(instance.username),
            from_email='from@example.com',
            recipient_list=[instance.email],
            fail_silently=False,
        )

@receiver(pre_delete, sender=Post)
def notify_before_post_delete(sender, instance, **kwargs):
    """Log or notify before a Post is deleted"""
    print(f"Post titled '{instance.title}' is about to be deleted.")