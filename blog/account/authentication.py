from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username: str = None, password: str = None):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        if check_password(password, user.password):
            return user
        return None

    def get_user(self, user_id: int):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
