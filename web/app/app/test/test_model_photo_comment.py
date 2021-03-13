"""
Test models PhotoComment
"""
from time import sleep

from django.db import models
from django.test import TestCase

from app.models import PhotoComment, User, Photo, Setting
from photobook.celery import app


class PhotoCommentTest(TestCase):
    """
    Tests for Photo model
    """
    @classmethod
    def setUpTestData(cls):
        app.conf.update(CELERY_ALWAYS_EAGER=True)
        User.objects.create(username='admin', password='12345', email='si-nn@mail.ru')
        Photo.objects.create(name='Test photo name',
                             original_file='test.jpg',
                             small_file='test.jpg',
                             webp_file='test.jpg',
                             user=User.objects.get(pk=1))
        PhotoComment.objects.create(
            photo=Photo.objects.get(pk=1),
            text='Test comment',
            user=User.objects.get(pk=1),
        )

    def test_text_field_label(self):
        """
        Test "text" field. Check label
        :return:
        """
        comment = PhotoComment.objects.get(id=1)
        field_label = comment._meta.get_field('text').verbose_name

        self.assertEqual(field_label, 'text', 'Field "Text" has wrong label')

    def test_text_field_type(self):
        """
        Test "text" field. Check type
        :return:
        """
        comment = PhotoComment.objects.get(id=1)
        field = comment._meta.get_field('text')

        self.assertTrue(isinstance(field, models.TextField), 'Field "Text" has wrong type')

    def test_text_field_max_length(self):
        """
        Test "text" field. Check max length
        :return:
        """
        comment = PhotoComment.objects.get(id=1)
        field_length = comment._meta.get_field('text').max_length

        self.assertEqual(field_length, 2000, 'Field "text" has wrong max length')

    def test_text_field_blank(self):
        """
        Test "text" field. Check blank attribute
        :return:
        """
        comment = PhotoComment.objects.get(id=1)
        field_blank = comment._meta.get_field('text').blank

        self.assertFalse(field_blank, 'Field "text" has wrong blank attribute')

    def test_add_date_field_label(self):
        """
        Test "add_date" field. Check label
        :return:
        """
        comment = PhotoComment.objects.get(id=1)
        field_label = comment._meta.get_field('add_date').verbose_name

        self.assertEqual(field_label, 'add date', 'Field "add_date" has wrong label')

    def test_add_date_auto_now_add(self):
        """
        Test "add_date" field. Check auto now add
        :return:
        """
        comment = PhotoComment.objects.get(pk=1)

        self.assertTrue(comment._meta.get_field('add_date').auto_now_add,
                        msg='Field "add_date" has no attribute auto_now_add')

    def test_add_date_type(self):
        """
        Test "add_date" field. Check type
        :return:
        """
        comment = PhotoComment.objects.get(id=1)
        field = comment._meta.get_field('add_date')

        self.assertTrue(isinstance(field, models.DateTimeField),
                        msg='Field "add_date" is not DateTimeField type')

    def test_user_field_type(self):
        """
        Test "user" field. Check type
        :return:
        """
        comment = PhotoComment.objects.get(pk=1)
        field = comment._meta.get_field('user')

        self.assertEqual(type(field), models.ForeignKey, msg='Field photo is not ForeignKey type')

    def test_user_field_relation_with_user(self):
        """
        Test "user" field. Check relation
        :return:
        """
        comment = PhotoComment.objects.get(pk=1)

        self.assertEqual(type(comment.user), User, msg='Field related with wrong model')

    def test_user_field_label(self):
        """
        Test "user" field. Check label
        :return:
        """
        comment = PhotoComment.objects.get(pk=1)
        field_label = comment._meta.get_field('user').verbose_name

        self.assertEqual(field_label, 'user', 'Field "user" has wrong label')

    def test_photo_field_type(self):
        """
        Test "photo" field. Check type
        :return:
        """
        comment = PhotoComment.objects.get(pk=1)
        field = comment._meta.get_field('photo')

        self.assertEqual(type(field), models.ForeignKey, msg='Field photo is not ForeignKey type')

    def test_photo_field_relation_with_user(self):
        """
        Test "photo" field. Check relation
        :return:
        """
        comment = PhotoComment.objects.get(pk=1)

        self.assertEqual(type(comment.photo), Photo, msg='Field related with wrong model')

    def test_photo_field_label(self):
        """
        Test "photo" field. Check label
        :return:
        """
        comment = PhotoComment.objects.get(pk=1)
        field_label = comment._meta.get_field('photo').verbose_name

        self.assertEqual(field_label, 'photo', 'Field "photo" has wrong label')
