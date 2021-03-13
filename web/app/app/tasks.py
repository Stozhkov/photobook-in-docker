"""
Tasks for Celery
"""

import logging

from io import BytesIO

import boto3
from PIL import Image
from resizeimage import resizeimage

from django.core.files import File
from django.core.mail import send_mail
from django.conf import settings

from photobook.celery import app


def send_email(subject, message, from_email, to_email):
    """
    Task for sending e-mail
    :param subject:
    :param message:
    :param from_email:
    :param to_email:
    :return:
    """
    try:
        send_mail(subject,
                  message,
                  from_email,
                  [to_email],
                  fail_silently=False)
    except Exception as err:
        logging.warning("Error send e-mail. %s" % err)


def make_small_file(photo_id):
    """
    Task for making small photo
    :param photo_id:
    :return:
    """

    from app.models import Photo

    photo = Photo.objects.get(pk=photo_id)
    image = photo.original_file

    file_name = image.name.split('/')[-1]

    image_obj = Image.open(image)
    file_format = image_obj.format
    width, height = image_obj.size

    image_obj.convert('RGB')

    if width > height:
        image_obj = resizeimage.resize_width(image_obj, 150)
    else:
        image_obj = resizeimage.resize_height(image_obj, 150)

    thumb_io = BytesIO()

    image_obj.save(thumb_io, file_format, quality=90)
    file_object = File(thumb_io, name=file_name)

    photo.small_file = file_object
    photo.save()


@app.task
def make_webp_file(photo_id):
    """
    Task for making webp photo.
    :param photo_id:
    :return:
    """

    from app.models import Photo

    photo = Photo.objects.get(pk=photo_id)
    image = photo.original_file

    file_name = image.name.split('/')[-1]

    image_obj = Image.open(image)
    image_obj.convert('RGB')

    thumb_io = BytesIO()
    new_file_name = '.'.join(file_name.split('.')[:-1]) + '.webp'

    image_obj.save(thumb_io, 'webp', quality=90)
    file_object = File(thumb_io, name=new_file_name)

    photo.webp_file = file_object
    photo.save()

@app.task
def make_files(photo_id):
    """
    Task for running "make_small_file" and "make_webp_file" one by one.
    :param photo_id:
    :return:
    """
    make_webp_file(photo_id)
    make_small_file(photo_id)


@app.task(bind=True)
def delete_file_from_s3(self, path):
    try:
        s3 = boto3.client(
            "s3", aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                         Key='media/' + path)

        return True
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
