from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """Manager for User model"""


class User(AbstractBaseUser):
    """User model"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    email = models.EmailField(max_length=255, unique=True, blank=True)
    cnic = models.CharField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    name = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=255, default='male')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
