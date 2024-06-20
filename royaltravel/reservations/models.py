from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from datetime import timedelta, date

from django.template.loader import render_to_string

from reservations.utils import generate_reservation_pdf

# რეზერვაციის მოდელი საჭირო ველებით
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reservation_number = models.AutoField(primary_key=True)
    reservation_reference = models.CharField(max_length=10, unique=True, blank=True, editable=False)
    start_date = models.DateField()
    end_date = models.DateField(blank=True)
    number_of_people = models.PositiveIntegerField(default=1)
    full_name = models.CharField(max_length=200)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    tour = models.ForeignKey('tours.Tour', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f'{self.reservation_reference} - {self.user}'

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.tour.duration-1)
        self.total_price = self.number_of_people * self.tour.price_per_person
        super().save(*args, **kwargs)
        # self.send_confirmation_email()
    # ფორმის ვალიდურობის შემოწმება და შესაბამისი ერორები
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.number_of_people > 6:
            raise ValidationError('Number of people cannot be more than 6')
        if self.start_date < (date.today() + timedelta(days=7)):
            raise ValidationError('Start date must be at least 1 week from now')
    # რეზერვაციის შემნის მომენტში წერილისა და პდფ ფაილის დაგენერირება და წარმატებით დაჯავშნის შემთხვევაში
    # მომხმარებლისთვის გაგზავნა
    def send_confirmation_email(self):
        subject = 'Reservation Confirmation'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = self.user.email
        text_content = render_to_string('reservations/reservation_confirmation_email.txt', {'reservation': self})
        html_content = render_to_string('reservations/reservation_confirmation_email.html', {'reservation': self})
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        pdf = generate_reservation_pdf(self)
        email.attach(f'Reservation_{self.reservation_reference}.pdf', pdf.read(), 'application/pdf')
        email.send()

    # პოსტერი რომელიც გაყვება რეზერვაციას რენდერის დროს (იგივე პოსტერი რაც დაჯავშნილ ტურს ქონდა)
    @property
    def image(self):
        return self.tour.poster.url if self.tour.poster else None

# Create your models here.
