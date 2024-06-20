from django.urls import path, reverse_lazy

from django.urls import path

from reservations.views import ReservationListView
from .views import TourListView, TourDetailView, TourCreateView, TourUpdateView, TourDeleteView, \
    PropertyTourView, PropertyReservationView, export_reservations_view

# დინამიური რაუთინგი ტურებისთვის
urlpatterns = [
    path('tours/', TourListView.as_view(), name='tour-list'),
    path('tours/<int:pk>/', TourDetailView.as_view(), name='tour-detail'),
    path('tours/create/', TourCreateView.as_view(), name='tour-create'),
    path('tours/<int:pk>/update/', TourUpdateView.as_view(), name='tour-update'),
    path('tours/<int:pk>/delete/', TourDeleteView.as_view(), name='tour-delete'),
    path('property/tours/', PropertyTourView.as_view(), name='property-tours'),
    path('poperty/reservations/', PropertyReservationView.as_view(), name='property-reservations'),
    path('property/reservations/export', export_reservations_view, name='export-reservations' )
]
