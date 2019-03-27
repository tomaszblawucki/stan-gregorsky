from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from enum import Enum
import datetime
# uses_app #

class UserRoles(Enum):
    REG = 'Regular employee'
    MAN = 'Project manager'


## UWAGA nie może być NONE i coś innego - zaimplementować mechanizm zmiany!!
class Proffessions(Enum):
    NONE = 'Not assigned'
    PROG = 'Programmer'
    TEST = 'Tester'
    MAN  = 'Project manager'
    ARCH = 'System architect'
    ADMN = 'System administrator'
    #Et cetera




class UserManager(BaseUserManager):

    def create_user(self, email, password, name, surname, birth_date=None):
        print("MODEL:", self.model)
        if not email: raise ValueError("email required")
        if not password: raise ValueError("password required")
        if not name: raise ValueError("name required")
        if not surname: raise ValueError("surname required")
        user_obj = self.model(
            email = self.normalize_email(email),
            name = name,
            surname = surname,
            birth_date = birth_date)
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password, name='derp', surname='derpington', birth_date=None):
        user_obj = self.create_user(email, password, name, surname, birth_date)
        user_obj.staff=True
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email, password, name='derp', surname='admin_derp', birth_date=None):
        user_obj = self.create_user(email, password, name, surname, birth_date)
        user_obj.staff=True
        user_obj.admin=True
        user_obj.save(using=self._db)
        return user_obj

class ResetPasswordToken(models.Model):
    email = models.EmailField(max_length=255)
    token = models.CharField(max_length=5)
    expire_date = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=1))

class Proffession(models.Model):
    proffession_name = models.CharField(max_length=20)
    proffession_description = models.TextField(max_length=1024, blank=True, default='')
    # choices=[(tag.name, tag.value) for tag in Proffessions])

    def __str__(self):
        return self.proffession_name




class User(AbstractBaseUser):

    username = None
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100, default='derp')
    surname = models.CharField(max_length=100, default='derpington')
    birth_date = models.DateField(default=None, blank=True, null=True)
    register_date = models.DateTimeField(auto_now_add=True, blank=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=True) #status użytkownika
    role = models.CharField(max_length=15,
                            choices=[(tag.name, tag.value) for tag in UserRoles],
                            default=UserRoles.REG) #Rola użytkownika w systemie (Uprawnienia)
    proffession = models.ManyToManyField(Proffession)#Specjalność

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
