from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class Patient(models.Model):
    """Patient model"""
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)

    weight = models.FloatField(null=True)
    height = models.FloatField(null=True)
    date_of_birth = models.DateTimeField(null=True)

    guardian_name = models.CharField(max_length=255, blank=True)
    guardian_contact = models.CharField(max_length=255, blank=True)
    guardian_relationship = models.CharField(max_length=255, blank=True)
    guardian_address = models.CharField(max_length=255, blank=True)

    def __repr__(self):
        return self.user.cnic

    class Meta:
        app_label = 'user'


class UserManager(BaseUserManager):
    """Manager for User model"""
    def create_user(self, cnic, password, **extra_fields):
        """Creates and saves a new user"""
        user = self.model(cnic, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, cnic, password, **extra_fields):
        """Creates and save a new superuser"""
        user = self.create_user(cnic, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()


class User(AbstractBaseUser, PermissionsMixin):
    """User model"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    email = models.EmailField(max_length=255, unique=True, blank=True)
    contact = models.CharField(max_length=255, blank=True)
    cnic = models.CharField(max_length=255, unique=True)
    emergency_contact = models.CharField(max_length=255, blank=True)

    name = models.CharField(max_length=255, blank=True)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)

    gender = models.CharField(max_length=255, default='male')

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='created_users')
    updated_by = models.ForeignKey('User', on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='updated_users')

    USERNAME_FIELD = 'cnic'

    @property
    def role(self):
        return self.patient

    def __repr__(self):
        return self.email

    class Meta:
        app_label = 'user'


class MedicalHistory(models.Model):
    """Medical History model"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    type = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    happened_at = models.DateTimeField(null=True)

    patient = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='created_medical_histories')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='updated_medical_histories')

    def __repr__(self):
        return f'{self.type} - {self.description}'

    class Meta:
        app_label = 'record'


class Visit(models.Model):
    """Visit model"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    purpose = models.TextField(blank=True)
    visited_at = models.DateTimeField()

    patient = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   null=True, related_name='created_visits')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   null=True, related_name='updated_visits')

    def __repr__(self):
        return self.visitedAt

    class Meta:
        app_label = 'record'


class Prescription(models.Model):
    """Prescription model"""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    medicine = models.CharField(max_length=255)
    dose = models.CharField(max_length=255, blank=True)
    frequency = models.CharField(max_length=255, blank=True)
    notes = models.TextField()

    patient = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='created_prescriptions')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='updated_prescriptions')

    def __repr__(self):
        return self.medicine

    class Meta:
        app_label = 'record'


class Allergy(models.Model):
    """Allergy model"""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    patient = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='created_allergies')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='updated_allergies')

    def __repr__(self):
        return self.name

    class Meta:
        app_label = 'record'
