"""Module containing views for managing ads."""
from datetime import date
from decimal import Decimal

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import LoginView as BaseLoginView
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import AdForm, CustomSignUpForm
from .models import AdEntry, AdType, UserProfile


class SignUpView(generic.CreateView):
    """View for user sign-up."""
    form_class = CustomSignUpForm
    success_url = reverse_lazy("login")
    template_name = "account/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        user_profile = UserProfile(user=self.object)
        user_profile.save()
        return response

class CustomLoginView(BaseLoginView):
    """Customized login view."""
    form_class = AuthenticationForm
    success_url = "/ads/ad_summary/"
    template_name = "account/login.html"

    def form_valid(self, form):
        """Check if the form is valid and authenticate the user."""
        email = form.cleaned_data['username']  # Assuming email field is used for authentication
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(self.get_success_url())
        return self.form_invalid(form)

@login_required
def calculate_reimbursement(request, ad_type, ads_run, actual_spend):
    """Calculate reimbursement for the given ad type, number of ads run, and actual spend."""
    if not isinstance(request.user, AnonymousUser):
        ad = AdType.objects.get(ad_code=str(ad_type))
        cost_share_rate = Decimal(ad.cost_share_rate)
        total_cost = Decimal(actual_spend) * ads_run
        cost_sharing = total_cost * cost_share_rate
        reimbursement = total_cost - cost_sharing
        return cost_sharing, reimbursement
    return HttpResponseForbidden("You are not authenticated.")

@login_required
def ad_input(request):
    """View function for handling ad input form."""
    if request.method == "POST":
        form = AdForm(request.POST)
        if form.is_valid():
            ad_type = form.cleaned_data["ad_type"].ad_code
            ads_run = form.cleaned_data["ads_run"]
            actual_spend = form.cleaned_data["actual_spend"]
            cost_sharing, reimbursement = calculate_reimbursement(
                request, ad_type, ads_run, actual_spend
            )
            ad_entry = AdEntry(
                ad_type=AdType.objects.get(ad_code=str(ad_type)),
                date=date.today(),
                ads_run=ads_run,
                actual_spend=actual_spend,
                cost_sharing=cost_sharing,
                reimbursement=reimbursement,
            )
            ad_entry.save()
            return redirect("ad_summary")
    else:
        form = AdForm()
    return render(request, "ads/ad_input.html", {"form": form})

@login_required
def ad_summary(request):
    """View function for displaying ad summary."""
    ads = AdEntry.objects.all()
    summary_data = []

    for ad in ads:
        ad_type = ad.ad_type
        ads_run = ads.filter(ad_type=ad_type).aggregate(
            total_ads_run=Sum('ads_run')
            )['total_ads_run']
        ad_date = ad.date.strftime("%Y-%m-%d").strip("(),")
        total_spend = sum(ad.actual_spend for ad in ads.filter(ad_type=ad_type))
        cost_sharing = total_spend * ad_type.cost_share_rate
        reimbursement = total_spend - cost_sharing

        summary_data.append(
            {
                "ad_type": ad_type.ad_code,
                "ads_run": ads_run,
                "ad_date": ad_date,
                "total_spend": total_spend,
                "cost_sharing": cost_sharing,
                "reimbursement": reimbursement,
            }
        )
    unique_summary = {v["ad_type"]: v for v in summary_data}.values()

    return render(request, "ads/ad_summary.html", {"summary_data": unique_summary})

@login_required
def profile(request):
    """View for displaying user profile."""
    user_profile = request.user.userprofile
    return render(request, "account/profile.html", {"user_profile": user_profile})
