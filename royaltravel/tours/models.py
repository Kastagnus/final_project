import os

from PIL import Image
from django.db import models

# ტურის მოდელი შესაბამისი ველებით
class Tour(models.Model):
    title = models.CharField(max_length=50)
    duration = models.PositiveIntegerField(help_text="Duration in days (max 20 days)")
    description = models.TextField(max_length=2000)
    annotation = models.TextField(max_length=100)
    price_per_person = models.PositiveIntegerField(help_text="Price in $")
    poster = models.ImageField(default='tour.jpg', upload_to='tours')

    def __str__(self):
        return self.title

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.duration > 20:
            raise ValidationError('Duration cannot be more than 20 days')

    # ტურს გაწერილი აქვს დეფოლტ ფოტო, რომლის ცვლილებაც შესაძლებელა
    # ფუნქცია ამოწმებს ახალ ფოტოს მოყავს შესაბამის ზომებში და არქმევს შსაბამის სახელს და ინახავს ბაზაში
    # თუ ფოტოს დამატებით შეცვლა ხდება ამ ტურზე მიბმული ძველი ფოტო ჯერ წაიშლება და შემდგომ აიტვირთება ახალი
    # ამცირებს ბაზის ტვირთს
    def save(self, *args, **kwargs):

        # Only delete the old avatar if it's being updated and is not the default
        try:
            this = Tour.objects.get(id=self.id)
            control_path = this.poster.path
            control_directory = control_path.split("\\")[-2]
            if this.poster != self.poster and control_directory != "media":
                if os.path.isfile(this.poster.path):
                    this.poster.delete(save=False)
        except Tour.DoesNotExist:
            pass
        super().save(*args, **kwargs)

        this = Tour.objects.get(pk=self.pk)
        control_path = this.poster.path
        control_directory = control_path.split("\\")[-2]
        if self.poster and control_directory != "media":
            extension = self.poster.name.split('.')[-1]
            new_poster_name = f"tours/{self.pk}-poster.{extension}"
            if self.poster.name != new_poster_name:
                poster_path = os.path.join('media', new_poster_name)
                os.rename(self.poster.path, poster_path)
                self.poster.name = new_poster_name
                super().save(*args, **kwargs)

        if self.poster and os.path.isfile(self.poster.path) and control_directory != "media":
            img = Image.open(self.poster.path)
            if img.height > 150 or img.width > 150:
                output_size = (150, 150)
                img.thumbnail(output_size)
                img.save(self.poster.path)
                print(f"Resized avatar saved at: {self.poster.path}")


# Create your models here.
