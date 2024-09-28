from django.db import models

from common.models import CommonModel
from portfolio.utils import upload_to


class MediaFile(CommonModel):
    MEDIA_TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )

    title = models.CharField(max_length=255)
    file_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to=upload_to)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title
