"""
Tests for API get comment
"""

import json

from rest_framework import status
from rest_framework.test import APITestCase

from app.models import User, Photo, PhotoComment
from photobook.celery import app


class ApiTest(APITestCase):
    """
    Test API /photos/comment/<pk>/
    """
    access_token = ''

    def setUp(self):
        app.conf.update(CELERY_ALWAYS_EAGER=True)
        self.superuser = User.objects.create_superuser('dima', 'dima@gmail.com', 'dimapassword')
        self.superuser = User.objects.create_superuser('dima2', 'dima@gmail.com', 'dimapassword')
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

        PhotoComment.objects.create(text='12345',
                                    photo=Photo.objects.get(pk=1),
                                    user=User.objects.get(pk=1))

        Photo.objects.create(name='Test name2',
                             original_file='test.jpg',
                             small_file='test.jpg',
                             webp_file='test.jpg',
                             view_counter=0,
                             user=User.objects.get(pk=2))

        PhotoComment.objects.create(text='12345',
                                    photo=Photo.objects.get(pk=2),
                                    user=User.objects.get(pk=2))

        response = self.client.post('/api/v1/auth/jwt/create', self.data, format='json')
        self.access_token = json.loads(response.content.decode("UTF-8"))['access']

    def test_get_comment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = self.client.get('/api/v1/photos/comment/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Wrong response status code "{response.status_code}". Should be "200""')

    def test_get_comment_for_alien_private_photo(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = self.client.get('/api/v1/photos/comment/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         f'Wrong response status code "{response.status_code}". Should be "403""')

    def test_get_comment_for_alien_public_photo(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        photo = Photo.objects.get(pk=2)
        photo.is_public = True
        photo.save()

        response = self.client.get('/api/v1/photos/comment/2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Wrong response status code "{response.status_code}". Should be "200""')
