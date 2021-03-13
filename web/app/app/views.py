"""
View for "Photo book" project
"""

# import logging

from django.shortcuts import redirect
from django.db.models import F
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.models import Photo, PhotoOpening, PhotoComment
from .serializers import CommentDetailSerializer
from .serializers import PhotoCreateSerializer
from .serializers import PhotoDetailSerializer
from .serializers import PhotoListSerializer


class PhotoChangePrivacy(UpdateAPIView):
    """
    View for changing photo privacy
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoDetailSerializer

    def put(self, request, *args, **kwargs):
        """
        Put method
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        photo = Photo.objects.get(pk=kwargs['pk'])

        if photo.user.id != request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            obj = Photo.objects.get(id=kwargs['pk'])
            obj.is_public = not obj.is_public
            obj.save()
            return redirect('detail', pk=kwargs['pk'])


class PhotoCommentListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentDetailSerializer

    def get(self, request, *args, **kwargs):
        try:
            photo = Photo.objects.get(pk=kwargs['pk'])
        except Photo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            if photo.is_public or photo.user.id == request.user.id:
                comments = PhotoComment.objects.filter(photo=photo).order_by('-add_date')
                serializer = CommentDetailSerializer(comments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)


class CommentDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentDetailSerializer

    def get(self, request, *args, **kwargs):
        try:
            comment = PhotoComment.objects.get(pk=kwargs['pk'])
        except PhotoComment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            photo = comment.photo

            if photo.is_public or photo.user.id == request.user.id:
                serializer = CommentDetailSerializer(comment)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)


class CommentCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentDetailSerializer

    def post(self, request, *args, **kwargs):

        try:
            photo = Photo.objects.get(pk=request.data['photo'])
        except Photo.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if photo.is_public or photo.user.id == request.user.id:
            # _mutable = request.data._mutable
            # request.data._mutable = True
            request.data['user'] = request.user.id
            # request.data._mutable = _mutable

            return self.create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class PhotoDetailView(RetrieveUpdateDestroyAPIView):
    """
    Class for update photo name and detail view
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoDetailSerializer
    queryset = Photo.objects.all()

    def get(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=kwargs['pk'])

        if photo.user.id != request.user.id:
            if not photo.is_public:
                return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                Photo.objects.filter(pk=kwargs['pk']).update(view_counter=F('view_counter') + 1)

                PhotoOpening.objects.create(photo=Photo.objects.get(pk=kwargs['pk']))

                queryset = Photo.objects.get(id=kwargs['pk'])
        else:
            queryset = Photo.objects.get(id=kwargs['pk'], user=request.user.id)

        serializer = PhotoDetailSerializer(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        queryset = Photo.objects.filter(pk=kwargs['pk'],
                                        user=request.user.id).update(name=request.data['name'])
        if not queryset:
            return Response(data='Error.', status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = Photo.objects.filter(pk=kwargs['pk'], user=request.user.id)
            serializer = PhotoDetailSerializer(queryset, many=True)
            return Response(serializer.data)


class PhotoCreateView(CreateAPIView):
    """
    Class for creating new photo
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoCreateSerializer

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return self.create(request, *args, **kwargs)


class PhotoListView(ListAPIView):
    """
    Class for list view
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoListSerializer

    def get(self, request, *args, **kwargs):
        queryset = Photo.objects.filter(user=request.user.id)

        if not queryset:
            return Response(data='No photo for view', status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = PhotoListSerializer(queryset, many=True)
            return Response(serializer.data)


class PublicPhotoListView(PhotoListView):
    """
    Class for public list view
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoListSerializer

    def get(self, request, *args, **kwargs):
        queryset = Photo.objects.filter(is_public=True)

        if not queryset:
            return Response(data='No photos for view', status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = PhotoListSerializer(queryset, many=True)
            return Response(serializer.data)
