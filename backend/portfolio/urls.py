from django.urls import path
from backend.portfolio.views import upload_media, media_list

urlpatterns = [
    path('upload/', upload_media, name='upload_media'),
    path('media/', media_list, name='media_list'),
]