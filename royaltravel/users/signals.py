from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, CustomUser

# იღებს სიგნალს იმის შესახებ მომხმარებლის ბოლო ცვლილების დროს მოხდა თუ არა სტატუსის ცვლილეება
# თუ სტატუსი შეიცვალა არა-აქტიურიდან აქტიურზე ავტომატურად იქმენა მომხმარებლისტვის პროფილი
@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if not created and getattr(instance, '_is_activation_change', False):
        if not Profile.objects.filter(user=instance).exists():
            Profile.objects.create(user=instance)
        instance._is_activation_change = False
