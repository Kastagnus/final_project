from celery import shared_task
from django.utils.timezone import now
from .models import Reservation

# დავალება რომელიც გადაცემული აქვს სელერის, სრულდება მაშინ თუ მოდელში გაწერილი პირობა შესრულდა
@shared_task
def update_reservation_statuses():
    today = now().date()
    reservations = Reservation.objects.filter(status='active', end_date__lt=today)
    reservations.update(status='completed')


