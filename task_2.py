# TASK 2

"""Module defining Reimbursement class."""

import sys
from io import StringIO


class Reimbursement:
    """Class to describe spending for Ads and reimbursement."""

    def __init__(self):
        """Initialize the Reimbursement object."""
        self.ads = {
            '0011': {'cost_share_rate': 0.50, 'allowed_spend': 200, 'count': 0},
            '1011': {'cost_share_rate': 1.00, 'allowed_spend': (1000, 2000), 'count': 0},
            '1111': {'cost_share_rate': 0.75, 'allowed_spend': 500, 'count': 0},
            '1010': {'cost_share_rate': 0.90, 'allowed_spend': 750, 'count': 0}
        }

    def add_ad(self, ad_type):
        """Add an ad of the specific type."""
        if ad_type in self.ads:
            self.ads[ad_type]['count'] += 1
            return True
        return False

    def remove_ad(self, ad_type):
        """Remove an ad of the specific type."""
        if ad_type in self.ads and self.ads[ad_type]['count'] > 0:
            self.ads[ad_type]['count'] -= 1
            return True
        return False

    def print_ads(self):
        """Print the content of the Ads object."""
        print("Ad Type\tCostShareRate\tAllowedSpend\t\tCount")
        for ad_type, details in self.ads.items():
            allowed_spend = details['allowed_spend']
            if isinstance(allowed_spend, tuple):
                allowed_spend = f"${allowed_spend[0]} to ${allowed_spend[1]}"
            else:
                allowed_spend = f"${allowed_spend}"
            print(f"{ad_type}\t{details['cost_share_rate']}\t{allowed_spend}\t\t{details['count']}")

    def total_reimbursement(self):
        """Return the total amount of reimbursement."""
        total_reimbursement = 0
        for details in self.ads.values():
            total_reimbursement += details['count'] * details['cost_share_rate']
        return total_reimbursement

# Unit Tests
def test_reimbursement():
    """Unit test for the Reimbursement class."""
    reimbursement = Reimbursement()

    assert reimbursement.add_ad('0011') is True
    assert reimbursement.add_ad('1011') is True
    assert reimbursement.add_ad('1111') is True
    assert reimbursement.add_ad('1010') is True
    assert reimbursement.add_ad('invalid') is False

    assert reimbursement.remove_ad('0011') is True
    assert reimbursement.remove_ad('1011') is True
    assert reimbursement.remove_ad('1111') is True
    assert reimbursement.remove_ad('1010') is True
    assert reimbursement.remove_ad('invalid') is False

    reimbursement.add_ad('0011')
    reimbursement.add_ad('1011')
    reimbursement.add_ad('1111')
    reimbursement.add_ad('1010')
    expected_output = "Ad Type\tCostShareRate\tAllowedSpend\t\tCount\n"\
                      "0011\t0.5\t$200\t\t1\n"\
                      "1011\t1.0\t$1000 to $2000\t\t1\n"\
                      "1111\t0.75\t$500\t\t1\n"\
                      "1010\t0.9\t$750\t\t1\n"

    actual_output = capture_print_output(reimbursement.print_ads)
    print("Actual Output:\n", actual_output)
    print("Expected Output:\n", expected_output)
    print(actual_output == expected_output)
    assert actual_output == expected_output

    assert reimbursement.total_reimbursement() == 3.15

    print("All tests passed!")


def capture_print_output(func):
    """Capture the output of the print_ads method."""
    captured_output = StringIO()
    sys.stdout = captured_output
    func()
    sys.stdout = sys.__stdout__
    return captured_output.getvalue()


if __name__ == "__main__":
    test_reimbursement()
