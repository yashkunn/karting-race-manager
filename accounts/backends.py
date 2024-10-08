from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        users = user_model.objects.filter(email=username)
        if users.exists():
            user = users.first()
            if user.check_password(password):
                return user
        return None
