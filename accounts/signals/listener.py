from django.db.models import signals
from django.dispatch import receiver
from accounts.models import CustomUser, UserProfile, InstituteProfile


# creates a profile if the user is created
@receiver(signals.post_save, sender=CustomUser)
def create_user_profile(instance, created, **kwargs):
    if created:
        if instance.user_role == 'U':
            profile = UserProfile.objects.create(user=instance)
            profile.save()
        elif instance.user_role == "I":
            profile = InstituteProfile.objects.create(user=instance)
            profile.save()


