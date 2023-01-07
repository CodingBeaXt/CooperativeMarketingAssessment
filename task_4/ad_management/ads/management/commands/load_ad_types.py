"""Load AdTypes data into the database"""

from django.core.management.base import BaseCommand

from ads.models import AdType


class Command(BaseCommand):
    """Load AdTypes data into the database"""
    help = "Load AdTypes data into the database"

    def handle(self, *args, **kwargs):
        ad_types_data = [
            {"ad_code": "0011", "cost_share_rate": 0.50, "allowed_spend": 200},
            {"ad_code": "1011", "cost_share_rate": 1.00, "allowed_spend": (1000, 2000)},
            {"ad_code": "1111", "cost_share_rate": 0.75, "allowed_spend": 500},
            {"ad_code": "1010", "cost_share_rate": 0.90, "allowed_spend": 750},
        ]

        for ad_type_data in ad_types_data:
            AdType.objects.create(**ad_type_data)

        self.stdout.write(self.style.SUCCESS("AdTypes data loaded successfully"))
