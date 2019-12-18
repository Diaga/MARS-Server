from django.contrib import admin

from . import models


# User
admin.site.register(models.User)
admin.site.register(models.Patient)
admin.site.register(models.Nurse)
admin.site.register(models.Doctor)
admin.site.register(models.Admin)

# Record
admin.site.register(models.Allergy)
admin.site.register(models.MedicalHistory)
admin.site.register(models.Visit)
admin.site.register(models.Prescription)
