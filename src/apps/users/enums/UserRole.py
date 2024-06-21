
from django.db import models

class UserEnum(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    CLIENT = "CLIENT"