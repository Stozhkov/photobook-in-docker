"""
Tests for API change photo privacy
"""

import json

from rest_framework import status
from rest_framework.test import APITestCase

from app.models import PhotoOpening, User, Photo
from photobook.celery import app


class ApiTest(APITestCase):
    """
    Test API
    """
    access_token = ''

    def setUp(self):
        app.conf.update(CELERY_ALWAYS_EAGER=True)
        self.superuser = User.objects.create_superuser('dima', 'dima@gmail.com', 'dimapassword')
        self.data = {'username': 'dima', 'password': 'dimapassword'}

        self.client.login(
            username=self.data['username'],
            password=self.data['password'])

        Photo.objects.create(name='Test name',
                             original_file='test.jpg',
                             small_file='test.jpg',
                             webp_file='test.jpg',
                             view_counter=0,
                             user=User.objects.get(pk=1))

        PhotoOpening.objects.create(photo=Photo.objects.get(pk=1))

        response = self.client.post('/api/v1/auth/jwt/create', self.data, format='json')
        self.access_token = json.loads(response.content.decode("UTF-8"))['access']

    def test_change_privacy(self):

        """
        Test change photo privacy
        API: /api/v1/photo/<id>
        :return:
        """

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = self.client.get('/api/v1/photos/photo/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Wrong response status code "{response.status_code}". Should be "200""')

        self.assertEqual(Photo.objects.get(pk=1).is_public, False, 'Wrong "is_public" field')

        response = self.client.put('/api/v1/photos/photo/1/change_privacy/')

        self.assertEqual(response.status_code, status.HTTP_302_FOUND,
                         f'Wrong response status code "{response.status_code}". Should be "302""')

        self.assertEqual(Photo.objects.get(pk=1).is_public, True, 'Field "is_public" not changed.')

        response = self.client.put('/api/v1/photos/photo/1/change_privacy/')

        self.assertEqual(response.status_code, status.HTTP_302_FOUND,
                         f'Wrong response status code "{response.status_code}". Should be "302""')

        self.assertEqual(Photo.objects.get(pk=1).is_public, False, 'Field "is_public" not changed.')
