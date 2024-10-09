from django.urls import path, include
from rest_framework.routers import DefaultRouter

from portfolio.views import upload_media, MediaFileView, MediaFileListView, MediaPositionViewSet, \
    VideoThumbnailView

router = DefaultRouter()
router.register(r'media-positions', MediaPositionViewSet, basename='media-position')

urlpatterns = [
    path('upload/', upload_media, name='upload_media'),
    path('image/<uuid>', MediaFileView.as_view(), name='image-resize'),
    path('image-thumbnail/<uuid>', VideoThumbnailView.as_view(), name='media-thumbnail'),
    path('images/', MediaFileListView.as_view(), name='media-list'),
    path('', include(router.urls)),

]
