from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation
# სიგნალი რომელიც აფიქსირებს რეზერვაციის შექმნის მომენტს, აგენერირებს რეზერვაციის ნომერს და აგზავნი იმეილს
@receiver(post_save, sender=Reservation)
def generate_reference_code(sender, instance, created, **kwargs):
    if created and not instance.reservation_reference:
        instance.reservation_reference = f'RES{instance.reservation_number:06d}'
        instance.save()
        instance.send_confirmation_email()
