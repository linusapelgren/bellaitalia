from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone_number', 'guests', 'date', 'time')  # Remove 'created_at'
    search_fields = ('name', 'phone_number', 'date')
    list_filter = ('date', 'time')