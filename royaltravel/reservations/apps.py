from django.apps import AppConfig

# ვახდენთ სიგნალების იმპოტირებას რათა ავტომატური დავალებები შემცირდეს
class ReservationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservations'

    def ready(self):
        import reservations.signals
