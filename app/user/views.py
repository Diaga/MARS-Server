from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from . import serializers
from core.models import User
from core.permissions import check_permission, IsAdmin


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    """View set for User model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    queryset = User.objects.all()

    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        """Enforce scope"""
        user = self.request.user
        queryset = super(UserViewSet, self).get_queryset()

        if user.group == 'patient':
            queryset = queryset.filter(
                id=user.id
            )
        elif user.group == 'nurse':
            queryset = queryset.filter(
                patient__isnull=False
            ) | queryset.filter(
                id=user.id
            )
        elif user.group == 'doctor':
            queryset = queryset.filter(
                patient__isnull=False
            ) | queryset.filter(
                nurse__isnull=False
            ) | queryset.filter(
                id=user.id
            )
        userType = self.request.GET.get('type', None)
        if userType is not None:
        	if userType == 'self':
        		queryset = queryset.filter(id=user.id)
        	elif userType == 'patient':
        		queryset = queryset.filter(group='patient')    
        return queryset.all()

    def view_user(self, request, *args, **kwargs):
        """Return users"""
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_user(self, request, *args, **kwargs):
        """Wrapper around create method for view set distinction"""
        return self.create(request, *args, **kwargs)


class UserDetailViewSet(viewsets.GenericViewSet,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin):
    """Detail view set for User model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    queryset = User.objects.all()

    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        """Enforce scope"""
        user = self.request.user
        queryset = super(UserDetailViewSet, self).get_queryset()

        if user.group == 'patient':
            queryset = self.request.user
        elif user.group == 'nurse' or user.group == 'doctor':
            queryset = queryset.filter(
                patient__isnull=False
            )
        return queryset.all()

    def view_user_by_id(self, request, *args, **kwargs):
        """Wrapper around retrieve method for view set distinction"""
        return self.retrieve(request, *args, **kwargs)

    def update_user_by_id(self, request, *args, **kwargs):
        """Wrapper around update method for view set distinction"""
        return self.partial_update(request, *args, **kwargs)

    def destroy_user_by_id(self, request, *args, **kwargs):
        """Check if user is admin"""
        check_permission(IsAdmin, request, self)
        return self.destroy(request, *args, **kwargs)


class AuthTokenViewSet(ObtainAuthToken):
    """Custom token authentication view set"""

    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
