from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.backends import BaseBackend


class CustomBackend(BaseBackend):
    def authenticate(self, request, email=None, **kwargs):
        if not email:
            return None

        try:
            user = get_user_model().objects.get(email=email)
        except (get_user_model().DoesNotExist, MultipleObjectsReturned):
            return None

        return user

    def get_user(self, user_id):
        try:
            user = get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None

        return user
