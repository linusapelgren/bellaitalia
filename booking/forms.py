from django import forms
from .models import Reservation, OpeningHours
from datetime import datetime

class ReservationForm(forms.ModelForm):
    name = forms.CharField(label='Your Name', max_length=100)
    phone_number = forms.CharField(label='Phone Number', max_length=20)
    guests = forms.IntegerField(
        label='Number of Guests',
        min_value=1,
        widget=forms.NumberInput(attrs={'type': 'number', 'min': '1', 'max': '10', 'step': '1'})
    )
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'class': 'datepicker'}))
    time = forms.ChoiceField(label='Time', choices=[])

    def __init__(self, *args, **kwargs):
        fetch_available_times = kwargs.pop('fetch_available_times', None)
        super().__init__(*args, **kwargs)

        if self.data.get('date'):
            date = datetime.strptime(self.data['date'], '%Y-%m-%d').date()
        elif 'initial' in kwargs and 'date' in kwargs['initial']:
            date = kwargs['initial']['date']
        else:
            date = datetime.today().date()

        # Check if the date is closed
        day_of_week = date.weekday()  # Monday=0, Sunday=6
        try:
            opening_hours = OpeningHours.objects.get(day_of_week=day_of_week)
            if opening_hours.closed:
                available_times = []
            else:
                if fetch_available_times:
                    available_times = fetch_available_times(date)
                else:
                    available_times = []
        except OpeningHours.DoesNotExist:
            available_times = []

        self.fields['time'].choices = [(time_slot, time_slot) for time_slot in available_times]
        self.fields['date'].initial = date

    class Meta:
        model = Reservation
        fields = ['name', 'phone_number', 'guests', 'date', 'time']