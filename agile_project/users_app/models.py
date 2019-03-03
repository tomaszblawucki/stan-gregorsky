from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime
from enum import Enum

# Create your models here.

class UserRoles(Enum):
    REG = 'Regular employee'
    MAN = 'Project manager'


class UserManager(BaseUserManager):
    def create_user(self, email, password, name, surname, birth_date=None):
        if not email: raise ValueError("email required")
        if not password: raise ValueError("password required")
        if not name: raise ValueError("name required")
        if not surname: raise ValueError("surname required")
        user_obj = self.model(
            email = self.normalize_email(email),
            name = name,
            surname = surname,
            birth_date = birth_date)
        user_obs.set_password(password)
        user_obj.save(using=self._db)
        return user

class User(AbstractBaseUser):

    username = None
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birth_date = models.DateField()
    active = models.BooleanField(default=False) # can login
    role = models.CharField(max_length=3,
                            choices=[(tag, tag.value) for tag in UserRoles],
                            default=UserRoles.REG)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.is_admin
