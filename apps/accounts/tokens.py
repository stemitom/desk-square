from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class UserActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk)
            + text_type(timestamp)
            + text_type(user.is_email_verified)
        )


account_activation_token = UserActivationTokenGenerator()
account_password_reset_token = PasswordResetTokenGenerator()
