# tokens.py
from datetime import timedelta

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.utils import timezone

# ტოკენის გენერატორი რომელსაც ვიყენებთ მომხმრებლის იმეილით აქტივაციის დროს
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active))

    def check_token(self, user, token):
        if not super().check_token(user, token):
            return False
        expiration_date = user.last_token_generated + timedelta(minutes=2)
        return timezone.now() <= expiration_date

account_activation_token = AccountActivationTokenGenerator()
