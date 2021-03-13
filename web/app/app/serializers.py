"""
Serializers for "Photo book" project
"""

from django.conf import settings
from rest_framework import serializers
from app.models import PhotoComment
from app.models import Photo


class CommentDetailSerializer(serializers.ModelSerializer):
    """
    Detail serializer for PhotoComment model
    """
    class Meta:
        """
        Meta class
        """
        model = PhotoComment
        fields = '__all__'


class PhotoListSerializer(serializers.ModelSerializer):
    """
    List serializer for Photo model
    """
    class Meta:

        """
        Meta class
        """
        model = Photo
        fields = ('id', 'name', 'small_file', 'webp_file', 'user', 'view_counter')


class PhotoDetailSerializer(serializers.ModelSerializer):
    """
    Detail serializer for Photo model
    """
    class Meta:

        """
        Meta class
        """
        model = Photo
        read_only_fields = ('id', 'original_file', 'small_file', 'webp_file', 'user',
                            'view_counter', 'date_upload')
        fields = '__all__'


class PhotoCreateSerializer(serializers.ModelSerializer):
    """
    Detail serializer for Photo model
    """
    def validate(self, attrs):
        """
        Validate file parameters
        :param attrs:
        :return:
        """

        file_name = str(attrs['original_file'])
        file_extension = file_name.split('.')[-1]

        if file_extension.lower() not in settings.ALLOWED_FILE_TYPES:
            raise serializers.ValidationError('Wrong file type.')

        if len(attrs['original_file']) > settings.MAX_FILE_SIZE:
            raise serializers.ValidationError('File too large.')

        return attrs

    class Meta:

        """
        Meta class
        """
        model = Photo
        read_only_fields = ('view_counter', 'date_upload')
        fields = ('name', 'original_file', 'user')
