from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            email=instance.email,
            username=instance.username
        )
    else:
        try:
            profile = instance.profile
        except Profile.DoesNotExist:
            Profile.objects.create(
                user=instance,
                email=instance.email,
                username=instance.username
            )
            return

        updated = False
        if profile.email != instance.email:
            profile.email = instance.email
            updated = True
        if profile.username != instance.username:
            profile.username = instance.username
            updated = True
        if updated:
            # Only save if something actually changed
            profile.save(update_fields=['email', 'username'])

@receiver(post_save, sender=Profile)
def update_user_from_profile(sender, instance, **kwargs):
    user = instance.user
    updated = False
    if user.email != instance.email:
        user.email = instance.email
        updated = True
    if user.username != instance.username:
        user.username = instance.username
        updated = True
    if updated:
        # Prevent recursive save loop
        user.save(update_fields=['email', 'username'])
