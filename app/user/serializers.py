from django.contrib.auth import authenticate

from rest_framework import serializers

from core.models import User, Patient
from core.serializers import ModelBySerializer


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model"""

    class Meta:
        model = Patient
        fields = ('id', 'weight', 'height', 'date_of_birth',
                  'guardian_name', 'guardian_contact',
                  'guardian_relationship', 'guardian_address')
        read_only_fields = ('id', )


class UserSerializer(ModelBySerializer):
    """Serializer for User model"""

    role = serializers.SerializerMethodField('get_role')

    class Meta:
        model = User
        fields = ('id', 'email', 'contact', 'cnic', 'emergency_contact',
                  'first_name', 'middle_name', 'last_name', 'city',
                  'country', 'address', 'gender', 'patient', 'created_at',
                  'updated_at', 'created_by', 'updated_by')
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by',
                            'updated_by')
        write_only_fields = ('patient', )


class AuthTokenSerializer(serializers.Serializer):
    """Custom token authentication serializer"""
    email = serializers.EmailField()
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
