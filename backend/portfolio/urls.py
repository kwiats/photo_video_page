from django.urls import path
from portfolio.views import upload_media, media_list, MediaFileView, MediaFileListView

urlpatterns = [
    path('upload/', upload_media, name='upload_media'),
    path('media/', media_list, name='media_list'),
    path('image/<uuid>', MediaFileView.as_view(), name='image-resize'),
    path('images/', MediaFileListView.as_view(), name='media-list'),

]