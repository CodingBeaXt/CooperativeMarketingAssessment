"""Module containing models for managing ads."""

from django.contrib.auth.models import User
from django.db import models


class AdType(models.Model):
    """Represents a type of advertisement."""
    ad_code = models.CharField(max_length=10)
    cost_share_rate = models.FloatField()
    allowed_spend = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        """Metadata options for the AdType model."""
        app_label = "ads"


class AdEntry(models.Model):
    """Represents an entry for an advertisement."""
    ad_type = models.ForeignKey(AdType, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    ads_run = models.IntegerField()
    actual_spend = models.FloatField()
    cost_sharing = models.FloatField(default=0.0)
    reimbursement = models.FloatField(default=0.0)

    objects = models.Manager()


class UserProfile(models.Model):
    """Represents a profile for a user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
