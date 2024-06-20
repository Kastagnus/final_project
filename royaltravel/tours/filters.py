import django_filters
from reservations.models import Reservation

# ჯანგოს ფილტრის საშუალებით ქმნის ფილტრაციის სეტს მითითებული ველბის შესაბამისად
class ReservationFilter(django_filters.FilterSet):
    reservation_number = django_filters.CharFilter(field_name='reservation_reference', lookup_expr='match', label='Reservation Number')
    # reservation_user = django_filters.CharFilter(field_name='')
    status = django_filters.ChoiceFilter(choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], label='Status')

    class Meta:
        model = Reservation
        fields = ['reservation_reference', 'status']
