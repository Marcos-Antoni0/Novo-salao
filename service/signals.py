from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Service
from gemini_api.api import get_service_ai_bio

@receiver(pre_save, sender=Service)
def generate_service_description(sender, instance, **kwargs):
    if not instance.description:
        ai_bio = get_service_ai_bio(instance.name)
        instance.description = ai_bio