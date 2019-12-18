from rest_framework import serializers

from core.models import MedicalHistory, Visit, Allergy, Prescription
from core.serializers import ModelBySerializer
from user.serializers import UserSerializer


class MedicalHistorySerializer(ModelBySerializer):
    """Serializer for MedicalHistory model"""

    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    patient = UserSerializer(read_only=True)

    class Meta:
        model = MedicalHistory
        fields = ('id', 'type', 'description', 'happened_at',
                  'patient', 'created_at', 'updated_at', 'created_by',
                  'updated_by', 'patient')
        read_only_fields = ('id', 'created_at', 'updated_at',
                            'created_by', 'updated_by')


class VisitSerializer(ModelBySerializer):
    """Serializer for Visit model"""

    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    patient = UserSerializer(read_only=True)

    class Meta:
        model = Visit
        fields = ('id', 'purpose', 'visited_at',
                  'patient', 'created_at', 'updated_at', 'created_by',
                  'updated_by', 'patient')
        read_only_fields = ('id', 'created_at', 'updated_at',
                            'created_by', 'updated_by')


class AllergySerializer(ModelBySerializer):
    """Serializer for Allergy model"""

    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    patient = UserSerializer(read_only=True)

    class Meta:
        model = Allergy
        fields = ('id', 'name', 'description',
                  'patient', 'created_at', 'updated_at', 'created_by',
                  'updated_by', 'patient')
        read_only_fields = ('id', 'created_at', 'updated_at',
                            'created_by', 'updated_by')


class PrescriptionSerializer(ModelBySerializer):
    """Serializer for Prescription model"""

    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    patient = UserSerializer(read_only=True)

    class Meta:
        model = Prescription
        fields = ('id', 'medicine', 'dose', 'frequency', 'notes',
                  'patient', 'created_at', 'updated_at', 'created_by',
                  'updated_by', 'patient')
        read_only_fields = ('id', 'created_at', 'updated_at',
                            'created_by', 'updated_by')
