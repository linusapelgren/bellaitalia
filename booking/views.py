# bookings/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation
from datetime import datetime
from django.http import JsonResponse
from .utils import fetch_available_times, send_sms
from .forms import ReservationForm

def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST, fetch_available_times=fetch_available_times)
        if form.is_valid():
            reservation = form.save()
            send_sms(reservation.phone_number, reservation)
            print(f"Reservation created: {reservation.id}")
            return redirect('reservation_confirmation', reservation_id=reservation.id)
        else:
            print("Form errors:", form.errors)  # Print form errors to debug
    else:
        form = ReservationForm(fetch_available_times=fetch_available_times)

    return render(request, 'booking/make_reservation.html', {'form': form})

def reservation_confirmation(request, reservation_id):
    print(f"Confirming reservation: {reservation_id}")
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    print(f"Reservation {reservation_id} booked.")
    return render(request, 'booking/reservation_confirmation.html', {'reservation': reservation})

def get_available_times(request):
    date_str = request.GET.get('date')
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    times = fetch_available_times(date)
    return JsonResponse({'times': times})

def cancellation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    return render(request, 'booking/cancellation.html', {'reservation': reservation})

def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
  
    # Delete the reservation
    reservation.delete()
    
    # Print cancellation message
    print(f"Reservation {reservation_id} cancelled.")
    
    # Redirect to cancellation confirmation page
    return redirect('cancellation_confirmation')

def cancellation_confirmation(request):
    return render(request, 'booking/cancellation_confirmation.html')