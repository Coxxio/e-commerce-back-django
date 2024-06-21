from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

from ...apps.users.models import UserModel

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = UserModel.objects.filter(email=email).defer('person').first()
        except UserModel.DoesNotExist:
            return None
        else:
            if check_password(password, user.password):
                return user
        return None