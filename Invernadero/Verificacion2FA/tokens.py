from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    pass

account_activation_token = AccountActivationTokenGenerator()