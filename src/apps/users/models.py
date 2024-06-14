from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from .enums.UserRole import UserEnum
from ...common.models.BaseModel import BaseModel


class PersonModel(BaseModel):
    fullName = models.CharField(max_length=100, blank=False, null=False)
    phoneNumber = models.CharField(max_length=20, blank=True, null=True)
    codePostal = models.CharField(max_length=10, blank=False, null=False)
    country = models.CharField(max_length=20, blank=False, null=False)
    

class UserModel(AbstractBaseUser, BaseModel):
    
    email = models.EmailField('Email', max_length=50, unique=True)
    role = models.CharField(max_length=11 ,choices=UserEnum.choices, blank=False, null=False)
    person = models.ForeignKey(PersonModel, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self) -> str:
        return f'{self.person.name}'

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True
    
