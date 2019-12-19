from uuid import uuid4

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core import models
from core import utils
from .. import serializers


MEDICAL_HISTORY_VIEW = reverse('record:medical_history-view')


def medical_history_detail(pk):
    """Creates MEDICAL_HISTORY_DETAIL"""
    return reverse('record:medical_history-detail', args=[pk, ])


class MedicalHistoryPublicApiTests(TestCase):
    """Tests for Medical History Public API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_medical_history_get(self):
        """Test that get method is not allowed"""
        res = self.client.get(MEDICAL_HISTORY_VIEW)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_medical_history_post(self):
        """Test that post method is not allowed"""
        res = self.client.post(MEDICAL_HISTORY_VIEW)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_medical_history_detail_get(self):
        """Test that get method is not allowed"""
        res = self.client.get(medical_history_detail(uuid4()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_medical_history_detail_patch(self):
        """Test that patch method is not allowed"""
        res = self.client.patch(medical_history_detail(uuid4()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_medical_history_detail_delete(self):
        """Test that delete method is not allowed"""
        res = self.client.delete(medical_history_detail(uuid4()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class MedicalHistoryPrivateApiTests(TestCase):
    """Tests for Medical History Public API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.admin = utils.sample_user(group='admin')
        self.client.force_authenticate(user=self.admin)
        self.patient = utils.sample_user(cnic='sample_patient',
                                         group='patient')

    def test_medical_history_get(self):
        """Test that get method is allowed"""
        medical_history = utils.sample_medical_history(patient=self.patient)
        res = self.client.get(MEDICAL_HISTORY_VIEW)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0], serializers.MedicalHistorySerializer(
            medical_history
        ).data)

    def test_medical_history_post(self):
        """Test that post method is allowed"""
        payload = {'patient_id': self.patient.id}
        res = self.client.post(MEDICAL_HISTORY_VIEW, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(models.MedicalHistory.objects.filter(
            patient__id=self.patient.id
        ).exists())

    def test_medical_history_detail_get(self):
        """Test that get method is allowed"""
        medical_history = utils.sample_medical_history(patient=self.patient)
        res = self.client.get(medical_history_detail(medical_history.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializers.MedicalHistorySerializer(
            medical_history
        ).data)

    def test_medical_history_detail_patch(self):
        """Test that patch method is allowed"""
        medical_history = utils.sample_medical_history(patient=self.patient)
        payload = {'type': 'test'}
        res = self.client.patch(medical_history_detail(medical_history.id),
                                payload)
        medical_history.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['type'], payload['type'])

    def test_medical_history_detail_delete(self):
        """Test that delete method is allowed"""
        medical_history = utils.sample_medical_history(patient=self.patient)
        res = self.client.delete(medical_history_detail(medical_history.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.MedicalHistory.objects.filter(
            id=medical_history.id
        ).exists())
