from django.contrib import admin
from .models import Reservation, OpeningHours


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone_number', 'guests', 'date', 'time')
    search_fields = ('name', 'phone_number', 'date')
    list_filter = ('date', 'time')

@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('get_day_of_week_display', 'start_time', 'end_time', 'closed')
    fields = ['day_of_week', 'start_time', 'end_time', 'closed']
    list_filter = ('day_of_week',)
    ordering = ('day_of_week',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.closed:
            # Disable 'start_time' and 'end_time' if closed
            form.base_fields['start_time'].widget.attrs['readonly'] = True
            form.base_fields['end_time'].widget.attrs['readonly'] = True
        return form