from django.contrib.auth import authenticate

from rest_framework import serializers

from core.models import User, Patient, Nurse, Doctor, Admin
from core.serializers import ModelBySerializer


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model"""

    class Meta:
        model = Patient
        fields = ('id', 'weight', 'height', 'date_of_birth',
                  'guardian_name', 'guardian_contact',
                  'guardian_relationship', 'guardian_address')
        read_only_fields = ('id', )


class NurseSerializer(serializers.ModelSerializer):
    """Serializer for Nurse model"""

    class Meta:
        model = Nurse
        fields = ('id', 'qualification', 'institution', 'date_joined',
                  'start_timings', 'end_timings')
        read_only_fields = ('id', )


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor model"""

    class Meta:
        model = Doctor
        fields = ('id', 'speciality', 'qualification', 'medical_college',
                  'date_joined', 'start_timings', 'end_timings',
                  'nurse_assigned')
        read_only_fields = ('id', )


class AdminSerializer(serializers.ModelSerializer):
    """Serializer for Admin model"""

    class Meta:
        model = Admin
        fields = ('id', 'date_joined', 'start_timings', 'end_timings')
        read_only_fields = ('id', )


class UserSerializer(ModelBySerializer):
    """Serializer for User model"""

    role = serializers.SerializerMethodField('get_role')

    def get_role(self, obj):
        if obj.group == 'admin':
            return AdminSerializer(obj.admin).data
        elif obj.group == 'doctor':
            return DoctorSerializer(obj.doctor).data
        elif obj.group == 'nurse':
            return NurseSerializer(obj.nurse).data
        elif obj.group == 'patient':
            return PatientSerializer(obj.patient).data

    group = serializers.ChoiceField(
        choices={
            'patient': 'patient',
            'nurse': 'nurse',
            'doctor': 'doctor',
            'admin': 'admin'
        },
    )

    patient = PatientSerializer(write_only=True, allow_null=True)
    nurse = NurseSerializer(write_only=True, allow_null=True)
    doctor = DoctorSerializer(write_only=True, allow_null=True)
    admin = AdminSerializer(write_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'cnic', 'password', 'email', 'contact',
                  'emergency_contact', 'first_name', 'middle_name', 'last_name'
                  , 'city', 'country', 'address', 'gender', 'group', 'patient',
                  'created_at', 'updated_at', 'created_by', 'updated_by',
                  'admin', 'nurse', 'doctor', 'role')
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by',
                            'updated_by', 'role')

    def create(self, validated_data):
        group = validated_data.pop('group')
        password = validated_data.pop('password')

        patient_data = validated_data.pop('patient')
        nurse_data = validated_data.pop('nurse')
        doctor_data = validated_data.pop('doctor')
        admin_data = validated_data.pop('admin')

        user = super(UserSerializer, self).create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        group = validated_data.pop('group')
        password = validated_data.pop('password')
        user = super(UserSerializer, self).update(instance, validated_data)
        user.set_password(password)
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Custom token authentication serializer"""
    cnic = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Authenticate and return user"""
        cnic = attrs.get('cnic')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            cnic=cnic,
            password=password
        )

        if not user:
            msg = "Unable to authenticate with provided credentials"
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
