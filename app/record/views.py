from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from . import serializers
from core.models import MedicalHistory, Visit, Allergy, Prescription
from core.permissions import IsNotPatient


class MedicalHistoryViewSet(viewsets.GenericViewSet,
                            mixins.CreateModelMixin):
    """View set for MedicalHistory model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    queryset = MedicalHistory.objects.all()

    serializer_class = serializers.MedicalHistorySerializer

    def get_queryset(self):
        """Enforce scope"""
        user = self.request.user
        queryset = super(MedicalHistoryViewSet, self).get_queryset()
        if user.group == 'patient':
            queryset = queryset.filter(patient=user)
        return queryset.all()

    def view_medical_history(self, request, *args, **kwargs):
        """Return medical histories"""
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_medical_history(self, request, *args, **kwargs):
        """Wrapper around create method for view set distinction"""
        return self.create(request, *args, **kwargs)


class MedicalHistoryDetailViewSet(viewsets.GenericViewSet,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin):
    """Detail view set for Medical History model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, IsNotPatient]

    queryset = MedicalHistory.objects.all()

    serializer_class = serializers.MedicalHistorySerializer

    def get_queryset(self):
        """Enforce scope"""
        user = self.request.user
        queryset = super(MedicalHistoryDetailViewSet, self).get_queryset()
        if user.group == 'patient':
            queryset = queryset.filter(patient=user)
        return queryset.all()

    def view_medical_history_by_id(self, request, *args, **kwargs):
        """Wrapper around retrieve method for view set distinction"""
        return self.retrieve(request, *args, **kwargs)

    def update_medical_history_by_id(self, request, *args, **kwargs):
        """Wrapper around update method for view set distinction"""
        return self.partial_update(request, *args, **kwargs)

    def destroy_medical_history_by_id(self, request, *args, **kwargs):
        """Wrapper around delete method for view set distinction"""
        return self.destroy(request, *args, **kwargs)


class VisitViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin):
    """View set for Visit model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    queryset = Visit.objects.all()

    serializer_class = serializers.VisitSerializer

    def get_queryset(self):
        """Enforce scope"""
        user = self.request.user
        queryset = super(VisitViewSet, self).get_queryset()
        if user.group == 'patient':
            queryset = queryset.filter(patient=user)
        return queryset.all()

    def view_visit(self, request, *args, **kwargs):
        """Return visits"""
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_visit(self, request, *args, **kwargs):
        """Wrapper around create method for view set distinction"""
        return self.create(request, *args, **kwargs)


class VisitDetailViewSet(viewsets.GenericViewSet,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    """Detail view set for Visit model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, IsNotPatient]

    queryset = Visit.objects.all()

    serializer_class = serializers.VisitSerializer

    def get_queryset(self):
        """Enforce scope"""
        user = self.request.user
        queryset = super(VisitDetailViewSet, self).get_queryset()
        if user.group == 'patient':
            queryset = queryset.filter(patient=user)
        return queryset.all()

    def view_visit_by_id(self, request, *args, **kwargs):
        """Wrapper around retrieve method for view set distinction"""
        return self.retrieve(request, *args, **kwargs)

    def update_visit_by_id(self, request, *args, **kwargs):
        """Wrapper around update method for view set distinction"""
        return self.partial_update(request, *args, **kwargs)

    def destroy_visit_by_id(self, request, *args, **kwargs):
        """Wrapper around delete method for view set distinction"""
        return self.destroy(request, *args, **kwargs)


class PrescriptionViewSet(viewsets.GenericViewSet,
                          mixins.CreateModelMixin):
    """View set for Prescription model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    queryset = Prescription.objects.all()

    serializer_class = serializers.PrescriptionSerializer

    def get_queryset(self):
        """Enforce scope"""
        user = self.request.user
        queryset = super(PrescriptionViewSet, self).get_queryset()
        if user.group == 'patient':
            queryset = queryset.filter(patient=user)
        return queryset.all()

    def view_prescription(self, request, *args, **kwargs):
        """Return prescriptions"""
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_prescription(self, request, *args, **kwargs):
        """Wrapper around create method for view set distinction"""
        return self.create(request, *args, **kwargs)


class PrescriptionDetailViewSet(viewsets.GenericViewSet,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin):
    """Detail view set for Prescription model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, IsNotPatient]

    queryset = Prescription.objects.all()

    serializer_class = serializers.PrescriptionSerializer

    def get_queryset(self):
        """Enforce scope"""
        user = self.request.user
        queryset = super(PrescriptionDetailViewSet, self).get_queryset()
        if user.group == 'patient':
            queryset = queryset.filter(patient=user)
        return queryset.all()

    def view_prescription_by_id(self, request, *args, **kwargs):
        """Wrapper around retrieve method for view set distinction"""
        return self.retrieve(request, *args, **kwargs)

    def update_prescription_by_id(self, request, *args, **kwargs):
        """Wrapper around update method for view set distinction"""
        return self.partial_update(request, *args, **kwargs)

    def destroy_prescription_by_id(self, request, *args, **kwargs):
        """Wrapper around delete method for view set distinction"""
        return self.destroy(request, *args, **kwargs)


class AllergyViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin):
    """View set for Allergy model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    queryset = Allergy.objects.all()

    serializer_class = serializers.AllergySerializer

    def get_queryset(self):
        """Enforce scope"""
        user = self.request.user
        queryset = super(AllergyViewSet, self).get_queryset()
        if user.group == 'patient':
            queryset = queryset.filter(patient=user)
        return queryset.all()

    def view_allergy(self, request, *args, **kwargs):
        """Return allergies"""
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_allergy(self, request, *args, **kwargs):
        """Wrapper around create method for view set distinction"""
        return self.create(request, *args, **kwargs)


class AllergyDetailViewSet(viewsets.GenericViewSet,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin):
    """Detail view set for Allergy model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, IsNotPatient]

    queryset = Allergy.objects.all()

    serializer_class = serializers.AllergySerializer

    def get_queryset(self):
        """Enforce scope"""
        user = self.request.user
        queryset = super(AllergyDetailViewSet, self).get_queryset()
        if user.group == 'patient':
            queryset = queryset.filter(patient=user)
        return queryset.all()

    def view_allergy_by_id(self, request, *args, **kwargs):
        """Wrapper around retrieve method for view set distinction"""
        return self.retrieve(request, *args, **kwargs)

    def update_allergy_by_id(self, request, *args, **kwargs):
        """Wrapper around update method for view set distinction"""
        return self.partial_update(request, *args, **kwargs)

    def destroy_allergy_by_id(self, request, *args, **kwargs):
        """Wrapper around delete method for view set distinction"""
        return self.destroy(request, *args, **kwargs)

