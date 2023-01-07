"""Url patterns for Advertisments"""
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import CustomLoginView, SignUpView

urlpatterns = [
    path("ad_input/", views.ad_input, name="ad_input"),
    path("ad_summary/", views.ad_summary, name="ad_summary"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("profile/", views.profile, name="profile"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
