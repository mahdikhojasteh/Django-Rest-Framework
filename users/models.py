from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import date

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, username, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have email address')
        if not username:
            raise ValueError('Users must have username')
        
        user = self.model(
            email=email,
            username=username,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, username, password=None, **kwargs):
        user = self.create_user(
            email=email,
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
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    bio = models.TextField(max_length=2000, blank=True)
    birthdate = models.DateField(default=date.today)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['username']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username + ', ' + self.email
