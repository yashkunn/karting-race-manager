from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import RaceParticipation, Kart

@receiver(post_delete, sender=RaceParticipation)
def reset_kart_availability(sender, instance, **kwargs):
    kart = instance.kart
    kart.available_quantity += 1
    kart.save()