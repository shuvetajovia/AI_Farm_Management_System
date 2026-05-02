from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_farmer_profile(sender, instance, created, **kwargs):
    if created:
        from farmers.models import FarmerProfile
        FarmerProfile.objects.get_or_create(user=instance)