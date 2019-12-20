from uuid import uuid4

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from core import models
from core import utils
from .. import serializers


MEDICAL_HISTORY_VIEW = reverse('record:medical_history-view')
VISIT_VIEW = reverse('record:visit-view')
ALLERGY_VIEW = reverse('record:allergy-view')
PRESCRIPTION_VIEW = reverse('record:prescription-view')


def medical_history_detail(pk):
    """Creates MEDICAL_HISTORY_DETAIL"""
    return reverse('record:medical_history-detail', args=[pk, ])


def visit_detail(pk):
    """Creates VISIT_DETAIL"""
    return reverse('record:visit-detail', args=[pk, ])


def allergy_detail(pk):
    """Creates ALLERGY_DETAIL"""
    return reverse('record:allergy-detail', args=[pk, ])


def prescription_detail(pk):
    """Creates PRESCRIPTION_DETAIL"""
    return reverse('record:prescription-detail', args=[pk, ])


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
    """Tests for Medical History Private API"""

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
            id=res.data['id']
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


class VisitPublicApiTests(TestCase):
    """Tests for Visit Public API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_visit_get(self):
        """Test that get method is not allowed"""
        res = self.client.get(VISIT_VIEW)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_visit_post(self):
        """Test that post method is not allowed"""
        res = self.client.post(VISIT_VIEW)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_visit_detail_get(self):
        """Test that get method is not allowed"""
        res = self.client.get(visit_detail(uuid4()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_visit_detail_patch(self):
        """Test that patch method is not allowed"""
        res = self.client.patch(visit_detail(uuid4()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_visit_detail_delete(self):
        """Test that delete method is not allowed"""
        res = self.client.delete(visit_detail(uuid4()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class VisitPrivateApiTests(TestCase):
    """Tests for Visit Private API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.admin = utils.sample_user(group='admin')
        self.client.force_authenticate(user=self.admin)
        self.patient = utils.sample_user(cnic='sample_patient',
                                         group='patient')

    def test_visit_get(self):
        """Test that get method is allowed"""
        visit = utils.sample_visit(patient=self.patient)
        res = self.client.get(VISIT_VIEW)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0], serializers.VisitSerializer(
            visit
        ).data)

    def test_visit_post(self):
        """Test that post method is allowed"""
        payload = {'patient_id': self.patient.id,
                   'visited_at': timezone.now()}
        res = self.client.post(VISIT_VIEW, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(models.Visit.objects.filter(
            id=res.data['id']
        ).exists())

    def test_visit_detail_get(self):
        """Test that get method is allowed"""
        visit = utils.sample_visit(patient_id=self.patient.id)
        res = self.client.get(visit_detail(visit.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializers.VisitSerializer(
            visit
        ).data)

    def test_visit_detail_patch(self):
        """Test that patch method is allowed"""
        visit = utils.sample_visit(patient=self.patient)
        payload = {'purpose': 'test'}
        res = self.client.patch(visit_detail(visit.id),
                                payload)
        visit.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['purpose'], payload['purpose'])

    def test_visit_detail_delete(self):
        """Test that delete method is allowed"""
        visit = utils.sample_visit(patient=self.patient)
        res = self.client.delete(visit_detail(visit.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Visit.objects.filter(
            id=visit.id
        ).exists())


class AllergyPublicApiTests(TestCase):
    """Tests for Allergy Public API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_allergy_get(self):
        """Test that get method is not allowed"""
        res = self.client.get(ALLERGY_VIEW)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_allergy_post(self):
        """Test that post method is not allowed"""
        res = self.client.post(ALLERGY_VIEW)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_allergy_detail_get(self):
        """Test that get method is not allowed"""
        res = self.client.get(allergy_detail(uuid4()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_allergy_detail_patch(self):
        """Test that patch method is not allowed"""
        res = self.client.patch(allergy_detail(uuid4()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_allergy_detail_delete(self):
        """Test that delete method is not allowed"""
        res = self.client.delete(allergy_detail(uuid4()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AllergyPrivateApiTests(TestCase):
    """Tests for Allergy Private API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.admin = utils.sample_user(group='admin')
        self.client.force_authenticate(user=self.admin)
        self.patient = utils.sample_user(cnic='sample_patient',
                                         group='patient')

    def test_allergy_get(self):
        """Test that get method is allowed"""
        allergy = utils.sample_allergy(patient=self.patient)
        res = self.client.get(ALLERGY_VIEW)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0], serializers.AllergySerializer(
            allergy
        ).data)

    def test_allergy_post(self):
        """Test that post method is allowed"""
        payload = {'name': 'test_allergy', 'patient_id': self.patient.id}
        res = self.client.post(ALLERGY_VIEW, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(models.Allergy.objects.filter(
            id=res.data['id']
        ).exists())

    def test_allergy_detail_get(self):
        """Test that get method is allowed"""
        allergy = utils.sample_allergy(patient_id=self.patient.id)
        res = self.client.get(allergy_detail(allergy.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializers.AllergySerializer(
            allergy
        ).data)

    def test_allergy_detail_patch(self):
        """Test that patch method is allowed"""
        allergy = utils.sample_allergy(patient=self.patient)
        payload = {'name': 'test'}
        res = self.client.patch(allergy_detail(allergy.id),
                                payload)
        allergy.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], payload['name'])

    def test_allergy_detail_delete(self):
        """Test that delete method is allowed"""
        allergy = utils.sample_allergy(patient=self.patient)
        res = self.client.delete(allergy_detail(allergy.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Allergy.objects.filter(
            id=allergy.id
        ).exists())


class PrescriptionPublicApiTests(TestCase):
    """Tests for Prescription Public API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_prescription_get(self):
        """Test that get method is not allowed"""
        res = self.client.get(PRESCRIPTION_VIEW)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_prescription_post(self):
        """Test that post method is not allowed"""
        res = self.client.post(ALLERGY_VIEW)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_prescription_detail_get(self):
        """Test that get method is not allowed"""
        res = self.client.get(prescription_detail(uuid4()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_prescription_detail_patch(self):
        """Test that patch method is not allowed"""
        res = self.client.patch(prescription_detail(uuid4()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_prescription_detail_delete(self):
        """Test that delete method is not allowed"""
        res = self.client.delete(prescription_detail(uuid4()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrescriptionPrivateApiTests(TestCase):
    """Tests for Prescription Private API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.admin = utils.sample_user(group='admin')
        self.client.force_authenticate(user=self.admin)
        self.patient = utils.sample_user(cnic='sample_patient',
                                         group='patient')

    def test_prescription_get(self):
        """Test that get method is allowed"""
        prescription = utils.sample_prescription(patient=self.patient)
        res = self.client.get(PRESCRIPTION_VIEW)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0], serializers.PrescriptionSerializer(
            prescription
        ).data)

    def test_prescription_post(self):
        """Test that post method is allowed"""
        payload = {'medicine': 'test_prescription',
                   'patient_id': self.patient.id}
        res = self.client.post(PRESCRIPTION_VIEW, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(models.Prescription.objects.filter(
            id=res.data['id']
        ).exists())

    def test_prescription_detail_get(self):
        """Test that get method is allowed"""
        prescription = utils.sample_prescription(patient_id=self.patient.id)
        res = self.client.get(prescription_detail(prescription.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializers.PrescriptionSerializer(
            prescription
        ).data)

    def test_prescription_detail_patch(self):
        """Test that patch method is allowed"""
        prescription = utils.sample_prescription(patient=self.patient)
        payload = {'medicine': 'test'}
        res = self.client.patch(prescription_detail(prescription.id),
                                payload)
        prescription.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['medicine'], payload['medicine'])

    def test_prescription_detail_delete(self):
        """Test that delete method is allowed"""
        prescription = utils.sample_prescription(patient=self.patient)
        res = self.client.delete(prescription_detail(prescription.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Prescription.objects.filter(
            id=prescription.id
        ).exists())
