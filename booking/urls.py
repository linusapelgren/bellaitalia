from django.urls import path
from booking.views import make_reservation, reservation_confirmation, get_available_times, cancellation, cancel_reservation, cancellation_confirmation

urlpatterns = [
    path('make-reservation/', make_reservation, name='make_reservation'),
    path('reservation-confirmation/<int:reservation_id>/', reservation_confirmation, name='reservation_confirmation'),
    path('get-available-times/', get_available_times, name='get_available_times'),
    path('cancellation/<int:reservation_id>/', cancellation, name='cancellation'),
    path('cancel-reservation/<int:reservation_id>/', cancel_reservation, name='cancel_reservation'),  
    path('cancellation_confirmation/', cancellation_confirmation, name='cancellation_confirmation'),
]
