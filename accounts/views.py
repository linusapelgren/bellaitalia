from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from allauth.account.views import SignupView as AllauthSignupView
from .forms import CustomSignupForm
from .models import UserProfile
from allauth.account.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class CustomSignupView(AllauthSignupView):
    form_class = CustomSignupForm

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
