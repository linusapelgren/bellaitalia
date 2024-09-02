from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    guests = models.PositiveIntegerField()  # Ensures positive integer
    date = models.DateField()
    time = models.TimeField()  # Change to TimeField
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date} - {self.time}"

    def clean(self):
        if self.guests <= 0:
            raise ValidationError('Number of guests must be positive.')
        
class OpeningHours(models.Model):
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    closed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Opening Hour"
        verbose_name_plural = "Opening Hours"

    def __str__(self):
        return f"{self.get_day_of_week_display()}: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
