"""
Urls for application app
"""

from django.urls import path
from app.views import CommentCreateView
from app.views import CommentDetailView
from app.views import PhotoChangePrivacy
from app.views import PhotoCommentListView
from app.views import PhotoCreateView
from app.views import PhotoDetailView
from app.views import PhotoListView
from app.views import PublicPhotoListView


urlpatterns = [
    path('comment/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),
    path('comment/create/', CommentCreateView.as_view(), name='comment_create'),
    path('photo/<int:pk>/comments/', PhotoCommentListView.as_view(), name='comments'),

    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='detail'),
    path('photo/<int:pk>/change_privacy/', PhotoChangePrivacy.as_view()),
    path('photo/create/', PhotoCreateView.as_view()),
    path('public/', PublicPhotoListView.as_view()),
    path('', PhotoListView.as_view())
]
