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
