from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )

        subject = 'Welcome to DevSearch!'
        message = 'We are glad that you are with us!'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )


@receiver(post_save, sender=Profile)
def update_user(sender, created, instance, **kwargs):
    profile = instance
    user = profile.user

    if not created:
        user.username = profile.username
        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.email = profile.email
        user.save()


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except User.DoesNotExist:
        pass
