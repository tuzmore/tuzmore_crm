# backend/apps/users/tokens.py
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Generates a token for email verification (activation).
    Uses user primary key, timestamp, and is_active status.
    """
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"

# Instance to use in utils.py
account_activation_token = AccountActivationTokenGenerator()
