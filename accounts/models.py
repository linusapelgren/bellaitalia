from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

phone_number_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

class UserProfile(models.Model):
    """Model for user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        validators=[phone_number_regex]
    )

    def __str__(self):
        return f"{self.user.username} Profile"