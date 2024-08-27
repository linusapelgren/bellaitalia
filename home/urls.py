from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
]