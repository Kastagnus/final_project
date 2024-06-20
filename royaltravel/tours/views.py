from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Case, When, IntegerField
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from reservations.models import Reservation
from .filters import ReservationFilter
from .models import Tour
from django.shortcuts import redirect
from django.http import HttpResponse
from .utils import export_reservations_to_excel

# ტესტი რომელსაც გადის მომხმარებლი სანამ შეზღუდულ კონტენტს მიწვდება
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class PropertyTourView(StaffRequiredMixin,ListView):
    model = Tour
    template_name = 'tours/property_tours.html'
    context_object_name = 'tours'
    paginate_by = 3



class PropertyReservationView(StaffRequiredMixin,ListView):
    model = Reservation
    template_name = 'tours/property_reservations.html'
    context_object_name = 'reservations'
    filterset_class = ReservationFilter
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = self.filterset_class(self.request.GET, queryset=self.get_queryset())
        context['filter'] = filter
        context['reservations'] = filter.qs
        paginator = Paginator(context['reservations'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            custom_order=Case(
                When(status='active', then=0),
                When(status='completed', then=1),
                When(status='cancelled', then=2),
                default=3,
                output_field=IntegerField(),
            )
        ).order_by('custom_order', 'start_date')
        return queryset

def export_reservations_view(request):
    queryset = Reservation.objects.all()
    filterset = ReservationFilter(request.GET, queryset=queryset)
    filtered_queryset = filterset.qs
    return export_reservations_to_excel(filtered_queryset)


class TourListView(ListView):
    model = Tour
    template_name = 'tours/tour_list.html'
    context_object_name = 'tours'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-id')
        return queryset


class TourDetailView(DetailView):
    model = Tour
    template_name = 'tours/tour_detail.html'
    context_object_name = 'tour'

class TourCreateView(LoginRequiredMixin, StaffRequiredMixin,CreateView):
    model = Tour
    template_name = 'tours/tour_form.html'
    fields = ['title', 'duration', 'description', 'annotation', 'price_per_person', 'poster']
    success_url = reverse_lazy('property-tours')

class TourUpdateView(LoginRequiredMixin, StaffRequiredMixin,UpdateView):
    model = Tour
    template_name = 'tours/tour_form.html'
    fields = ['title', 'duration', 'description', 'annotation', 'price_per_person', 'poster']
    success_url = reverse_lazy('property-tours')

class TourDeleteView(LoginRequiredMixin, StaffRequiredMixin,DeleteView):
    model = Tour
    template_name = 'tours/tour_confirm_delete.html'
    success_url = reverse_lazy('property-tours')

# Create your views here.
