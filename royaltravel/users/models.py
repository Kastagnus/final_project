import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from PIL import Image
from royaltravel import settings

# აპლიკაციაში იუზერის მოდელი
class CustomUser(AbstractUser):
    DoesNotExist = None
    email = models.EmailField(unique=True, max_length=200)
    last_token_generated = models.DateTimeField(default=timezone.now)

    def __init__(self, *args, **kwargs):
        super(CustomUser, self).__init__(*args, **kwargs)
        self._initial_is_active = self.is_active
    # ვახდენთ იუზერის აქტიური სტატუს ქეშირებას რათა სიგნალებში დაფიქსირდეს ცვლილების მომენტი
    def save(self, *args, **kwargs):
        if self.pk and self.is_active != self._initial_is_active:
            self._is_activation_change = True
        else:
            self._is_activation_change = False

        super(CustomUser, self).save(*args, **kwargs)
        self._initial_is_active = self.is_active

# იუზერის პროფილის მოდელი
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatar.jpg', upload_to='profile_avatars')
    bio = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} profile'

    # იუზერს გაწერილი აქვს დეფოლტ ავატარი, რომლის ცვლილებაც შესაძლებელა
    # ფუნქცია ამოწმებს ახალ ფოტოს, მოყავს შესაბამის ზომებში და არქმევს შსაბამის სახელს და ინახავს ბაზაში
    # თუ ფოტოს დამატებით შეცვლა ხდება ამ იუზერზე მიბმული ძველი ავატარი ჯერ წაიშლება და შემდგომ აიტვირთება ახალი
    # ამცირებს ბაზის ტვირთს
    def save(self, *args, **kwargs):

        try:
            this = Profile.objects.get(id=self.id)
            control_path = this.avatar.path
            control_directory = control_path.split("\\")[-2]
            if this.avatar != self.avatar and control_directory != "media":
                if os.path.isfile(this.avatar.path):
                    this.avatar.delete(save=False)
        except Profile.DoesNotExist:
            pass
        super().save(*args, **kwargs)

        this = Profile.objects.get(id=self.id)
        control_path = this.avatar.path
        control_directory = control_path.split("\\")[-2]
        if self.avatar and control_directory != "media":
            extension = self.avatar.name.split('.')[-1]
            new_avatar_name = f"profile_avatars/{self.user.id}-avatar.{extension}"
            if self.avatar.name != new_avatar_name:
                avatar_path = os.path.join('media', new_avatar_name)
                os.rename(self.avatar.path, avatar_path)
                self.avatar.name = new_avatar_name
                super().save(*args, **kwargs)

        if self.avatar and os.path.isfile(self.avatar.path) and control_directory != "media":
            img = Image.open(self.avatar.path)
            if img.height > 150 or img.width > 150:
                output_size = (150, 150)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

# Create your models here.
