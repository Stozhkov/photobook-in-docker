"""
Test models
"""
from time import sleep

from django.db import models
from django.test import TestCase

from app.models import PhotoOpening, User, Photo, Setting
from photobook.celery import app


class ViewModelsTest(TestCase):
    """
    Tests for View model
    """
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='admin', password='12345')
        Photo.objects.create(name='Test photo name',
                             original_file='test.jpg',
                             small_file='test.jpg',
                             webp_file='test.jpg',
                             user=User.objects.get(pk=1))
        PhotoOpening.objects.create(photo=Photo.objects.get(pk=1))

    def test_photo_field_type(self):
        """
        Test "photo" field. Check type
        :return:
        """
        obj_view = PhotoOpening.objects.get(pk=1)
        field = obj_view._meta.get_field('photo')

        self.assertEqual(type(field), models.ForeignKey,
                         'Field photo is not ForeignKey type')

    def test_photo_field_relation_with_photo(self):
        """
        Test "photo" field. Check relation
        :return:
        """
        obj_view = PhotoOpening.objects.get(pk=1)

        self.assertEqual(type(obj_view.photo), Photo,
                         'Field related with wrong model')

    def test_photo_field_label(self):
        """
        Test "photo" field. Check label
        :return:
        """
        obj_view = PhotoOpening.objects.get(pk=1)
        field_label = obj_view._meta.get_field('photo').verbose_name

        self.assertEqual(field_label, 'photo',
                         'Field photo with wrong label')

    def test_date_view_auto_now_add(self):
        """
        Test "date_view" field. Check "auto add now"
        :return:
        """
        obj_view = PhotoOpening.objects.get(pk=1)

        self.assertTrue(obj_view._meta.get_field('date_view').auto_now_add,
                        'Field date_view has no attribute auto_now_add')

    def test_date_view_type(self):
        """
        Test "date_view" field. Check type
        :return:
        """
        obj_view = PhotoOpening.objects.get(id=1)
        field = obj_view._meta.get_field('date_view')

        self.assertTrue(isinstance(field, models.DateTimeField),
                        'Field date_view is not DateTimeField type')


class SettingModelTest(TestCase):
    """
    Tests for Setting model
    """
    @classmethod
    def setUpTestData(cls):
        Setting.objects.create(name='Test name', value='Test value')

    def test_name_field_label(self):
        """
        Test "name" field. Check label
        :return:
        """
        obj_view = Setting.objects.get(id=1)
        field_label = obj_view._meta.get_field('name').verbose_name

        self.assertEqual(field_label, 'name', 'Field "Name" has wrong label')

    def test_value_field_label(self):
        """
        Test "value" field. Check label
        :return:
        """
        obj_view = Setting.objects.get(id=1)
        field_label = obj_view._meta.get_field('value').verbose_name

        self.assertEqual(field_label, 'value', 'Field "Value" has wrong label')

    def test_name_field_type(self):
        """
        Test "name" field. Check type
        :return:
        """
        obj_view = Setting.objects.get(id=1)
        field = obj_view._meta.get_field('name')

        self.assertTrue(isinstance(field, models.CharField), 'Field "Name" has wrong type')

    def test_value_field_type(self):
        """
        Test "value" field. Check type
        :return:
        """
        obj_view = Setting.objects.get(id=1)
        field = obj_view._meta.get_field('value')

        self.assertTrue(isinstance(field, models.CharField), 'Field "Value" has wrong type')

    def test_name_field_max_length(self):
        """
        Test "name" field. Check max length
        :return:
        """
        obj_view = Setting.objects.get(id=1)
        field_length = obj_view._meta.get_field('name').max_length

        self.assertEqual(field_length, 25, 'Field "Name" has wrong max length')

    def test_value_field_max_length(self):
        """
        Test "value" field. Check max length
        :return:
        """
        obj_view = Setting.objects.get(id=1)
        field_length = obj_view._meta.get_field('value').max_length

        self.assertEqual(field_length, 250, 'Field "Value" has wrong max length')

    def test_name_field_blank(self):
        """
        Test "name" field. Check blank attribute
        :return:
        """
        obj_view = Setting.objects.get(id=1)
        field_blank = obj_view._meta.get_field('name').blank

        self.assertFalse(field_blank, 'Field "Name" has wrong blank attribute')

    def test_value_field_blank(self):
        """
        Test "value" field. Check blank attribute
        :return:
        """
        obj_view = Setting.objects.get(id=1)
        field_blank = obj_view._meta.get_field('value').blank

        self.assertFalse(field_blank, 'Field "Name" has wrong blank attribute')


class PhotoModelTest(TestCase):
    """
    Tests for Photo model
    """
    @classmethod
    def setUpTestData(cls):
        app.conf.update(CELERY_ALWAYS_EAGER=True)
        User.objects.create(username='admin', password='12345', email='si-nn@mail.ru')
        Photo.objects.create(name='Test photo name',
                             original_file='test.jpg',
                             user=User.objects.get(pk=1))
        # logging.warning(type(Photo.objects.get(name='Test photo name').original_file.file))
        PhotoOpening.objects.create(photo=Photo.objects.get(pk=1))

        sleep(5)

    # Name field tests
    def test_name_field_label(self):
        """
        Test "name" field. Check label
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_label = obj_view._meta.get_field('name').verbose_name

        self.assertEqual(field_label, 'name', 'Field "Name" has wrong label')

    def test_name_field_type(self):
        """
        Test "name" field. Check type
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field = obj_view._meta.get_field('name')

        self.assertTrue(isinstance(field, models.CharField), 'Field "Name" has wrong type')

    def test_name_field_max_length(self):
        """
        Test "name" field. Check max length
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_length = obj_view._meta.get_field('name').max_length

        self.assertEqual(field_length, 150, 'Field "Name" has wrong max length')

    def test_name_field_blank(self):
        """
        Test "name" field. Check blank attribute
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_blank = obj_view._meta.get_field('name').blank

        self.assertFalse(field_blank, 'Field "Name" has wrong blank attribute')

    # Original_file field tests
    def test_original_file_field_label(self):
        """
        Test "original_file" field. Check label
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_label = obj_view._meta.get_field('original_file').verbose_name

        self.assertEqual(field_label, 'original file', 'Field "original_file" has wrong label')

    def test_original_file_field_type(self):
        """
        Test "original_file" field. Check type
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field = obj_view._meta.get_field('original_file')

        self.assertTrue(isinstance(field, models.ImageField),
                        'Field "original_file" has wrong type')

    def test_original_file_field_upload_to(self):
        """
        Test "original_file" field. Check upload to
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_upload_to = obj_view._meta.get_field('original_file').upload_to

        self.assertEqual(field_upload_to, 'original',
                         'Field "original_file" has wrong attribute "upload_to"')

    def test_original_file_field_blank(self):
        """
        Test "original_file" field. Check blank
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_default = obj_view._meta.get_field('original_file').blank

        self.assertEqual(field_default, False,
                         'Field "original_file" has wrong blank attribute')

    def test_original_file_field_null(self):
        """
        Test "original_file" field. Check null
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_default = obj_view._meta.get_field('original_file').null

        self.assertEqual(field_default, False,
                         'Field "original_file" has wrong null attribute')

    # Small_file field tests
    def test_small_file_field_label(self):
        """
        Test "small_file" field. Check label
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_label = obj_view._meta.get_field('small_file').verbose_name

        self.assertEqual(field_label, 'small file', 'Field "small_file" has wrong label')

    def test_small_file_field_type(self):
        """
        Test "small_file" field. Check type
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field = obj_view._meta.get_field('small_file')

        self.assertTrue(isinstance(field, models.ImageField), 'Field "small_file" has wrong type')

    def test_small_file_field_upload_to(self):
        """
        Test "small_file" field. Check upload to
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_upload_to = obj_view._meta.get_field('small_file').upload_to

        self.assertEqual(field_upload_to, 'small',
                         'Field "small_file" has wrong attribute "upload to"')

    def test_small_file_field_default(self):
        """
        Test "small_file" field. Check default
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_default = obj_view._meta.get_field('small_file').default

        self.assertEqual(field_default, 'no-image.png', 'Field "small_file" has wrong default')

    # Webp_file field tests
    def test_webp_file_field_label(self):
        """
        Test "webp_file" field. Check label
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_label = obj_view._meta.get_field('webp_file').verbose_name

        self.assertEqual(field_label, 'webp file', 'Field "webp_file" has wrong label')

    def test_webp_file_field_type(self):
        """
        Test "webp_file" field. Check type
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field = obj_view._meta.get_field('webp_file')

        self.assertTrue(isinstance(field, models.ImageField), 'Field "webp_file" has wrong type')

    def test_webp_file_field_upload_to(self):
        """
        Test "webp_file" field. Check upload to
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_upload_to = obj_view._meta.get_field('webp_file').upload_to

        self.assertEqual(field_upload_to, 'webp',
                         'Field "webp_file" has wrong attribute "upload to"')

    def test_webp_file_field_default(self):
        """
        Test "webp_file" field. Check default
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_default = obj_view._meta.get_field('webp_file').default

        self.assertEqual(field_default, 'no-image.png',
                         'Field "webp_file" has wrong default attribute')

    # Date_upload field tests
    def test_date_upload_field_label(self):
        """
        Test "date_upload" field. Check label
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_label = obj_view._meta.get_field('date_upload').verbose_name

        self.assertEqual(field_label, 'date upload', 'Field "date_upload" has wrong label')

    def test_date_upload_auto_now_add(self):
        """
        Test "date_upload" field. Check auto now add
        :return:
        """
        obj_view = Photo.objects.get(pk=1)

        self.assertTrue(obj_view._meta.get_field('date_upload').auto_now_add,
                        msg='Field "date_upload" has no attribute auto_now_add')

    def test_date_upload_type(self):
        """
        Test "date_upload" field. Check type
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field = obj_view._meta.get_field('date_upload')

        self.assertTrue(isinstance(field, models.DateTimeField),
                        msg='Field "date_upload" is not DateTimeField type')

    # View_counter field tests
    def test_view_counter_field_label(self):
        """
        Test "view_counter" field. Check label
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_label = obj_view._meta.get_field('view_counter').verbose_name

        self.assertEqual(field_label, 'view counter', 'Field "view_counter" has wrong label')

    def test_view_counter_field_type(self):
        """
        Test "view_counter" field. Check type
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field = obj_view._meta.get_field('view_counter')

        self.assertTrue(isinstance(field, models.PositiveIntegerField),
                        'Field "view_counter" has wrong type')

    def test_view_counter_field_default(self):
        """
        Test "view_counter" field. Check default
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_default = obj_view._meta.get_field('view_counter').default

        self.assertEqual(field_default, 0, 'Field "view_counter" has wrong default')

    # User field tests
    def test_user_field_type(self):
        """
        Test "user" field. Check type
        :return:
        """
        obj_view = Photo.objects.get(pk=1)
        field = obj_view._meta.get_field('user')

        self.assertEqual(type(field), models.ForeignKey, msg='Field photo is not ForeignKey type')

    def test_user_field_relation_with_user(self):
        """
        Test "user" field. Check relation
        :return:
        """
        obj_view = Photo.objects.get(pk=1)

        self.assertEqual(type(obj_view.user), User, msg='Field related with wrong model')

    def test_user_field_label(self):
        """
        Test "user" field. Check label
        :return:
        """
        obj_view = Photo.objects.get(pk=1)
        field_label = obj_view._meta.get_field('user').verbose_name

        self.assertEqual(field_label, 'user', 'Field "user" has wrong label')

    def test_is_public_field_label(self):
        """
        Test "is_public" field. Check label.
        :return:
        """
        photo = Photo.objects.get(pk=1)
        field_label = photo._meta.get_field('is_public').verbose_name

        self.assertEqual(field_label, 'is public', 'Field "is_public" has wrong label')

    def test_is_public_field_type(self):
        """
        Test "is_public" field. Check type.
        :return:
        """
        photo = Photo.objects.get(pk=1)
        field = photo._meta.get_field('is_public')

        self.assertTrue(isinstance(field, models.BooleanField),
                        'Field "is_public" has wrong type')

    def test_is_public_field_default(self):
        """
        Test "is_public" field. Check default attribute.
        :return:
        """
        obj_view = Photo.objects.get(id=1)
        field_default = obj_view._meta.get_field('is_public').default

        self.assertEqual(field_default, False, 'Field "is_public" has wrong default')
