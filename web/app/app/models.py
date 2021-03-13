"""
Models for "Photo book" project.
"""
import logging

from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.db import models
from django.contrib.auth.models import User

from app.tasks import make_files, delete_file_from_s3


class Photo(models.Model):
    """
    This model for photo file.
    """
    name = models.CharField(max_length=150, blank=False)
    original_file = models.ImageField(upload_to='original', blank=False, null=False)
    small_file = models.ImageField(upload_to='small', default='no-image.png')
    webp_file = models.ImageField(upload_to='webp', default='no-image.png')
    date_upload = models.DateTimeField(auto_now_add=True)
    view_counter = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Save model and run celery tasks.
        :param args:
        :param kwargs:
        :return:
        """
        super().save(*args, **kwargs)

        if self.small_file.name == 'no-image.png' and self.webp_file.name == 'no-image.png':
            make_files.delay(self.id)

    def __str__(self):
        """
        Return instance name
        :return:
        """
        return str(self.name)


class PhotoComment(models.Model):
    """
    This model for comments
    """
    text = models.TextField(max_length=2000, blank=False)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class PhotoOpening(models.Model):
    """
    This model for count views
    """
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    date_view = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.photo.name} - {self.date_view}'


class Setting(models.Model):
    """
    This model for settings
    """
    name = models.CharField(max_length=25, blank=False)
    value = models.CharField(max_length=250, blank=False)

    def __str__(self):
        return f'{self.name} - {self.value}'


@receiver(post_delete, sender=Photo)
def delete_file_hook(sender, instance, using, **kwargs):
    """
    Hook for deleting files from running tasks deleting files.
    :param sender:
    :param instance:
    :param using:
    :param kwargs:
    :return:
    """
    delete_file_from_s3.delay(instance.original_file.name)
    delete_file_from_s3.delay(instance.small_file.name)
    delete_file_from_s3.delay(instance.webp_file.name)
