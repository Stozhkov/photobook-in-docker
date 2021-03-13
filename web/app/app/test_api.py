"""
Tests for API
"""

import ast
import json
import logging
from time import sleep

from rest_framework import status
from rest_framework.test import APITestCase

from app.models import PhotoOpening, User, Photo
from photobook.celery import app
from app.functions import generate_file_name, generate_photo_file


class ApiAuthTest(APITestCase):
    """
    Test Auth API
    """
    access_token = ''

    def setUp(self):
        self.superuser = User.objects.create_superuser('dima', 'dima@gmail.com', 'dimapassword')
        self.client.login(username='dima', password='dimapassword')
        self.data = {'username': 'dima', 'password': 'dimapassword'}

        Photo.objects.create(name='Test name',
                             original_file='test.jpg',
                             small_file='test.jpg',
                             webp_file='test.jpg',
                             view_counter=1,
                             user=User.objects.get(pk=1))

        PhotoOpening.objects.create(photo=Photo.objects.get(pk=1))

    def test_register_user(self):
        """
        Test registering new user.
        API: /api/v1/auth/users/
        :return:
        """
        data = {'username': 'user1',
                'password': 'userpassword',
                'email': 'test@mail.ru'}

        error_message = ''

        response = self.client.post('/api/v1/auth/users/', data=data, format='json')
        status_code = response.status_code

        self.assertEqual(status_code, 201,
                         f'Wrong status code "{status_code}" in response. Should be "201".')

        try:
            created_user = User.objects.get(username=data['username'])
        except User.DoesNotExist as error:
            created_user = None
            error_message = error

        self.assertEqual(type(created_user), User, error_message)

    def test_can_get_token(self):

        """
        Test getting access tocen
        API: /api/v1/auth/jwt/create
        :return:
        """

        response = self.client.post('/api/v1/auth/jwt/create', self.data, format='json')
        status_code = response.status_code

        self.assertEqual(status_code, status.HTTP_200_OK,
                         f'Wrong response status code "{status_code}". Should be "200""')

        self.assertTrue('access' in json.loads(response.content.decode("UTF-8")),
                        f'No "access" token in response. {response.content}')


class ApiTest(APITestCase):
    """
    Test API
    """
    access_token = ''

    # def tearDownClass(cls):


    def setUp(self):
        app.conf.update(CELERY_ALWAYS_EAGER=True)
        self.superuser = User.objects.create_superuser('dima', 'dima@gmail.com', 'dimapassword')
        self.client.login(username='dima', password='dimapassword')
        self.data = {'username': 'dima', 'password': 'dimapassword'}

        Photo.objects.create(name='Test name',
                             original_file='test.jpg',
                             small_file='test.jpg',
                             webp_file='test.jpg',
                             view_counter=1,
                             user=User.objects.get(pk=1))

        PhotoOpening.objects.create(photo=Photo.objects.get(pk=1))

        response = self.client.post('/api/v1/auth/jwt/create', self.data, format='json')
        self.access_token = json.loads(response.content.decode("UTF-8"))['access']

    def test_getting_photo_list(self):

        """
        Test getting photo list
        API: /api/v1/list/
        :return:
        """

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get('/api/v1/photos/')

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Wrong response status code "{response.status_code}". Should be "200""')

        self.assertNotEqual(response.content, b'[]',
                            f'Wrong response. Get empty list "{response.content}"')

    def test_upload_photo(self):
        """
        Test getting photo list
        API: /api/v1/list/
        :return:
        """

        file_name = generate_file_name()
        file_name_webp = file_name.split('.')[0] + '.webp'

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        data = {
            'name': 'Test file 2',
            'original_file': generate_photo_file(file_name),
            'user': User.objects.get(username='dima').id
        }

        response = self.client.post('/api/v1/photos/photo/create/', data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         f'Wrong response status code "{response.status_code}". Should be "201""')

        sleep(3)

        photo = Photo.objects.get(name='Test file 2')

        self.assertEqual(data['name'], photo.name, 'Wrong "name" field')
        self.assertEqual('original/' + file_name, photo.original_file.name,
                         'Wrong "original_file" field')
        self.assertEqual('small/' + file_name, photo.small_file.name, 'Wrong "small_file" field')
        self.assertEqual('webp/' + file_name_webp, photo.webp_file.name, 'Wrong "webp_file" field')
        self.assertEqual(photo.view_counter, 0, 'Wrong "view_counter" field')
        self.assertEqual(photo.user.username, self.data['username'], 'Wrong "user" field')

    def test_get_photo(self):

        """
        Test getting photo list
        API: /api/v1/photo/<id>
        :return:
        """

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = self.client.get('/api/v1/photos/photo/1/', format='json')
        response_decode = json.loads(response.content.decode("UTF-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Wrong response status code "{response.status_code}". Should be "200""')

        self.assertEqual('Test name', response_decode['name'], 'Wrong "name" field')
        self.assertNotEqual(response_decode['original_file'],
                            'no-image.png', 'Wrong "original_file" field')

        self.assertNotEqual(response_decode['small_file'], 'no-image.png',
                            'Wrong "small_file" field')

        self.assertNotEqual(response_decode['webp_file'], 'no-image.png',
                            'Wrong "webp_file" field')
        self.assertNotEqual(response_decode['view_counter'], 0, 'Wrong "webp_file" field')

    def test_change_photo_name(self):

        """
        Test getting photo list
        API: /api/v1/photo/<id>
        :return:
        """

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        new_photo_name = 'New photo name'

        data = {
            'name': new_photo_name
        }

        response = self.client.put('/api/v1/photos/photo/1/', data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Wrong response status code "{response.status_code}". Should be "200""')

        photo = Photo.objects.get(pk=1)
        self.assertEqual(photo.name, new_photo_name, 'Wrong "name" field')
