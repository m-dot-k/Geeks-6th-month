from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager
from datetime import date

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    dob = models.DateField(null = True, blank= True)
    username = models.CharField(max_length=50, null = True, blank = True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.CharField(null=True, blank=True)

    objects = CustomUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email or ""
    
    def age(self):
        if self.dob:
            today = date.today()
            dob_extra = 1
            if self.dob.month < today.month:
                dob_extra = 0
            elif self.dob.month == today.month:
                if self.dob.day < today.day:
                    dob_extra = 0
            return today.year - self.dob.year - dob_extra
            # return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day)) - сокращенный вариант
        return None