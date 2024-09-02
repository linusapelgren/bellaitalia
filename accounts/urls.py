from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    CustomSignupView,
    profile,
)

urlpatterns = [
    path("signup/", CustomSignupView.as_view(), name="account_signup"),
    path("profile/", login_required(profile), name="profile"),
]