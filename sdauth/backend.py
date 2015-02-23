from django.contrib.auth.backends import ModelBackend
from django.conf import settings

from sdauth.models import User


class ModelBackend(ModelBackend):
    """
    Authenticate against stored username and password, plus check company.
    """

    def authenticate(self, username=None, password=None, request=None, agency=None, **kwargs):
        user = None

        if user is None:
            user = User.objects.filter(email=username, is_admin=True).first()

        if user is None:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            User().set_password(password)
            return

        if not user.check_password(password):
            return

        return user
