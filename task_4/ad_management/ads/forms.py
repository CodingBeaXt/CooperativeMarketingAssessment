"""Forms for advertisements"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import AdType


class AdForm(forms.Form):
    """Form for calculating ad details."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ad_type'].label_from_instance = self.label_from_ad_type_instance

    ad_type = forms.ModelChoiceField(queryset=AdType.objects.all())
    ads_run = forms.IntegerField(min_value=1)
    actual_spend = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2)

    def label_from_ad_type_instance(self, obj):
        """Custom method to display ad_code."""
        return obj.ad_code


class CustomSignUpForm(UserCreationForm):
    """Form for custom user signup."""
    email = forms.EmailField(max_length=254, help_text="Enter a valid email address")

    class Meta:
        """Metadata options for the Custom Sign up form."""
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )
