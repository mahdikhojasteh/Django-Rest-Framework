import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField

class CustomUserManager(BaseUserManager):
    
    def create_user(self, username, mobile, password=None, **kwargs):
        if not username:
            raise ValueError('Users must have username')
        if not mobile:
            raise ValueError('Users must have email address')
        
        user = self.model(
            mobile=mobile,
            username=username,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, username, mobile, password=None, **kwargs):
        user = self.create_user(
            mobile=mobile,
            username=username,
            password=password,
            **kwargs
        )
        user.is_admin = True
        # user.is_staff = True
        # user.is_superuser = True
        user.save(using=self._db)
        
        return username
    
    
class User(AbstractBaseUser):
    class Roles(models.IntegerChoices):
        guest = 1
        host = 2

    username = models.CharField(max_length=30, unique=True)
    mobile = PhoneNumberField(unique=True)
    mobile_verified = models.BooleanField(default=False)
    verify_code = models.CharField(max_length=10, blank=True)
    email = models.EmailField(max_length=60, unique=True, blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    bio = models.TextField(max_length=2000, blank=True)
    birthdate = models.DateField(default=date.today)
    role = models.IntegerField(choices=Roles.choices, default=Roles.guest)

    # This should potentially be an encrypted field
    jwt_key = models.UUIDField(default=uuid.uuid4)
    
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username + ', ' + self.mobile.as_e164
