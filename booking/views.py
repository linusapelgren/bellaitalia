from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation
from datetime import datetime
from django.http import JsonResponse
from .utils import fetch_available_times, send_sms
from .forms import ReservationForm
from django.contrib.auth.decorators import login_required
from accounts.views import profile
from .models import OpeningHours

@login_required
def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST, fetch_available_times=fetch_available_times)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user  # Assign the current logged-in user
            reservation.save()  # Save the reservation to the database
            send_sms(reservation.phone_number, reservation)  # Send SMS confirmation
            print(f"Reservation created: {reservation.id}")
            return redirect('reservation_confirmation', reservation_id=reservation.id)
        else:
            print("Form errors:", form.errors)
    else:
        initial_data = {
            'name': request.user.get_full_name(),
            'phone_number': '',
        }
        form = ReservationForm(initial=initial_data, fetch_available_times=fetch_available_times)

    return render(request, 'booking/make_reservation.html', {'form': form})

def reservation_confirmation(request, reservation_id):
    print(f"Confirming reservation: {reservation_id}")
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    print(f"Reservation {reservation_id} booked.")
    return render(request, 'booking/reservation_confirmation.html', {'reservation': reservation})

def get_available_times(request):
    date_str = request.GET.get('date')
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'times': []})

    # Get the day of the week for the selected date
    day_of_week = selected_date.weekday()  # Monday=0, Sunday=6

    # Check if the selected day is closed
    try:
        opening_hours = OpeningHours.objects.get(day_of_week=day_of_week)
        if opening_hours.closed:
            return JsonResponse({'times': []})
    except OpeningHours.DoesNotExist:
        return JsonResponse({'times': []})

    # Fetch available times if the day is not closed
    time_slots = fetch_available_times(selected_date)
    return JsonResponse({'times': time_slots})

def cancellation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    return render(request, 'booking/cancellation.html', {'reservation': reservation})

def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    reservation.delete()
    print(f"Reservation {reservation_id} cancelled.")
    return redirect('cancellation_confirmation')

def cancellation_confirmation(request):
    return render(request, 'booking/cancellation_confirmation.html')

@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation_confirmation', reservation_id=reservation.id)
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'booking/edit_reservation.html', {'form': form, 'reservation': reservation})

def update_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        # Handle form submission and update reservation
        # For example:
        reservation.guests = request.POST['guests']
        reservation.date = request.POST['date']
        reservation.time = request.POST['time']
        reservation.save()
        return redirect('profile')  # Redirect after successful update
    # Render form with reservation details
    return render(request, 'update_reservation.html', {'reservation': reservation})
