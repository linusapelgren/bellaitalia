from django.db import models
from django.conf import settings

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    guests = models.IntegerField()
    date = models.DateField()
    time = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.name} - {self.date} - {self.time}"
