from datetime import timedelta

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from tours.models import Tour
from .forms import ReservationForm
from .models import Reservation


class ReservationListView(ListView):
    model = Reservation
    template_name = 'reservations/reservation_list.html'
    context_object_name = 'reservations'
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'reservations/reservation_detail.html'
    context_object_name = 'reservation'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.kwargs['user_id'], pk=self.kwargs['pk'])
            return queryset
        return queryset


class ReservationCreateView(LoginRequiredMixin,CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/reservation_form.html'
    success_url = reverse_lazy('home')

    # ამოწმებს მომხმაებელს აქვს თუ არა მონიშნული ტური იმავე თარიღებზე
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        tour = get_object_or_404(Tour, id=self.kwargs.get('tour_id'))
        form.instance.tour = tour
        start_date = form.cleaned_data.get('start_date')
        end_date = start_date + timedelta(days=tour.duration)

        overlapping_reservations = Reservation.objects.filter(
            user=self.request.user,
            tour=tour,
            status='active',
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exclude(pk=user.pk)

        if overlapping_reservations.exists():
            form.add_error('start_date', 'You already have a reservation for this tour during the selected dates.')
            return self.form_invalid(form)
        messages.success(self.request, f'Your Confirmation has been sent to {self.request.user.email}')

        return super().form_valid(form)

class ReservationUpdateView(UpdateView):
    model = Reservation
    template_name = 'reservations/reservation_update_form.html'
    fields = ['start_date', 'number_of_people', 'full_name']
    success_url = reverse_lazy('home')
    context_object_name = 'reservation'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user, pk=self.kwargs['pk'])
            return queryset
        return queryset


    def form_valid(self, form):
        # user = self.kwargs['user_id']
        form.instance.user = self.object.user
        tour = self.object.tour
        form.instance.tour = tour
        start_date = form.cleaned_data.get('start_date')
        form.instance.end_date = start_date + timedelta(days=tour.duration-1)

        return super().form_valid(form)
# რეზერვაციის დაქენსელება
class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'reservations/reservation_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user, pk=self.kwargs['pk'])
        return queryset

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = 'cancelled'
        self.object.save()
        return redirect(self.success_url)





# Create your views here.
