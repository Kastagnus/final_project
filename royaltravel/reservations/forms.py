from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError

from .models import Reservation
# ფორმა რომელსაც ვარენდერებთ მომხმარებლისთვის რათა შეძლოს რეზერვაციის შექმნა
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'number_of_people', 'full_name']
        widgets = {
            'start_date': forms.DateInput(attrs={'id': 'id_start_date', 'type': 'text'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            start_date = cleaned_data.get('start_date')
            end_date = start_date + timedelta(days=self.tour.duration)

            # Check for overlapping reservations
            overlapping_reservations = Reservation.objects.filter(
                user=self.user,
                tour=self.tour,
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exclude(pk=self.instance.pk)

            if overlapping_reservations.exists():
                raise ValidationError('You already have a reservation for this tour during the selected dates.')

            return cleaned_data
