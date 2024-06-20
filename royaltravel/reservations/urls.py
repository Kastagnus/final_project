from django.urls import path
from .views import (ReservationListView, ReservationDetailView, ReservationCreateView, ReservationUpdateView,
                    ReservationDeleteView)
# დინამიური რაუთინგი რეზერვაციებისთვის
urlpatterns = [
    path('', ReservationListView.as_view(), name='reservation-list'),
    path('<int:user_id>/<int:pk>', ReservationDetailView.as_view(), name='reservation-detail'),
    path('create/<int:tour_id>/', ReservationCreateView.as_view(), name='reservation-create'),
    path('update/<int:user_id>/<int:pk>/', ReservationUpdateView.as_view(), name='reservation-update'),
    path('delete/<int:user_id>/<int:pk>', ReservationDeleteView.as_view(), name='reservation-cancel'),
]
