from django.db import models

from common.models import CommonModel
from portfolio.fields import ResolutionField
from portfolio.utils import content_file_name


class MediaFile(CommonModel):
    MEDIA_TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )

    title = models.CharField(max_length=255)
    file_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to=content_file_name)
    is_public = models.BooleanField(default=True)
    thumbnail = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class ProcessedMediaFile(CommonModel):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
    ]
    media_file = models.ForeignKey(MediaFile, on_delete=models.CASCADE)
    processed_file = models.FileField(upload_to=content_file_name)
    resolution = ResolutionField(null=True, blank=True)
    quality = models.IntegerField(default=75)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    def __str__(self):
        return self.media_file.title


class MediaPosition(CommonModel):
    name = models.CharField(max_length=255, blank=True)
    layout = models.JSONField()
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.name
