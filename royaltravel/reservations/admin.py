from django.contrib import admin

from reservations.models import Reservation

# ცვლის ადმინ პანელში რეზერვაციების მართვის შესაძლებლობებს ბიზნეს ლოგიკის შესაბამისად
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_reference', 'user', 'tour', 'start_date', 'end_date', 'number_of_people', 'status', 'total_price')
    search_fields = ('reservation_reference', 'user__username', 'tour__title', 'full_name')
    list_filter = ('status', 'start_date', 'end_date', 'tour__title')
    raw_id_fields = ('user', 'tour')
    readonly_fields = ('reservation_number', 'reservation_reference', 'total_price', 'end_date')
    fieldsets = (
        (None, {
            'fields': ('user', 'tour', 'start_date', 'end_date', 'number_of_people', 'full_name', 'status', 'total_price')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].queryset = form.base_fields['user'].queryset.filter(is_active=True)
        form.base_fields['tour'].queryset = form.base_fields['tour'].queryset.all()
        return form

    def save_model(self, request, obj, form, change):
        obj.check_and_update_status()
        super().save_model(request, obj, form, change)
admin.site.register(Reservation, ReservationAdmin)
