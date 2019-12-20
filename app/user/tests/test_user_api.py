from uuid import uuid4

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core import models
from core import utils
from .. import serializers


USER_VIEW = reverse('user:user-view')


def user_detail(pk):
    """Creates USER_DETAIL"""
    return reverse('user:user-detail', args=[pk, ])


class UserPublicApiTests(TestCase):
    """Test cases for User Public API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_user_get(self):
        """Test get method is not allowed"""
        res = self.client.get(USER_VIEW)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_post(self):
        """Test post method is not allowed"""
        res = self.client.post(USER_VIEW)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_detail_get(self):
        """Test get method is not allowed"""
        res = self.client.get(user_detail(uuid4()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_detail_patch(self):
        """Test patch method is not allowed"""
        res = self.client.patch(user_detail(uuid4()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_detail_delete(self):
        """Test delete method is not allowed"""
        res = self.client.delete(user_detail(uuid4()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UserPrivateApiTests(TestCase):
    """Test cases for User Private API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.admin = utils.sample_user(group='admin')
        self.client.force_authenticate(user=self.admin)

    def test_user_get(self):
        """Test get method is allowed"""
        res = self.client.get(USER_VIEW)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0], serializers.UserSerializer(
            self.admin
        ).data)

    def test_user_post(self):
        """Test post method is allowed"""
        payload = {'cnic': 'test_cnic', 'password': 'testpass',
                   'group': 'admin'}
        res = self.client.post(USER_VIEW, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(models.User.objects.filter(
            id=res.data['id']
        ).exists())

    def test_user_detail_get(self):
        """Test get method is allowed"""
        res = self.client.get(user_detail(self.admin.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializers.UserSerializer(
            self.admin
        ).data)

    def test_user_detail_patch(self):
        """Test patch method is allowed"""
        payload = {'cnic': 'test'}
        res = self.client.patch(user_detail(self.admin.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['cnic'], payload['cnic'])

    def test_user_detail_delete(self):
        """Test delete method is allowed"""
        res = self.client.delete(user_detail(self.admin.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.User.objects.filter(
            id=self.admin.id
        ).exists())
