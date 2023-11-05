from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
import uuid
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        if email is None:
            raise TypeError('Email is required')
        
        email=self.normalize_email(email)
        user = self.model(email=email,  **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self, email, password=None, **extra_fields):
        if password is None:
            raise TypeError('Password is required')
        
        user = self.create_user(email, password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(max_length=250, unique=True)
    name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='upload/profile', blank=True, null=True)
    otp = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_lawyer = models.BooleanField(default=False)
    is_google_user = models.BooleanField(default=False)
   

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token)
        }
    

class Client(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=True, null=True)
    account_type = models.CharField(max_length=250, blank=True, null=True)
    account_usecase = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name
