from django.utils import timezone
from . import models


def sample_user(cnic='sample_user', password='testpass', group=None,
                **extra_fields):
    """Creates a sample user in the system"""
    user = models.User.objects.create_user(
        cnic=cnic, password=password, **extra_fields
    )
    if group is not None:
        if group == 'patient':
            user.patient = models.Patient.objects.create()
        elif group == 'nurse':
            user.nurse = models.Nurse.objects.create()
        elif group == 'doctor':
            user.doctor = models.Doctor.objects.create()
        elif group == 'admin':
            user.admin = models.Admin.objects.create()
        user.save()
    return user


def sample_medical_history(**extra_fields):
    """Creates a sample medical history"""
    return models.MedicalHistory.objects.create(**extra_fields)


def sample_visit(visited_at=timezone.now(), **extra_fields):
    """Creates a sample visit"""
    return models.Visit.objects.create(visited_at=visited_at, **extra_fields)


def sample_allergy(name='test_allergy', **extra_fields):
    """Creates a sample allergy"""
    return models.Allergy.objects.create(name=name, **extra_fields)


def sample_prescription(medicine='test_medicine', **extra_fields):
    """Creates a sample prescription"""
    return models.Prescription.objects.create(medicine=medicine,
                                              **extra_fields)
