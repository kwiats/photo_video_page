from django.urls import reverse
from rest_framework import serializers

from common.serializers import CommonSerializer
from portfolio.models import MediaFile, MediaPosition


class MediaFileSerializer(CommonSerializer):
    file = serializers.SerializerMethodField()
    fileType = serializers.CharField(source='file_type')

    class Meta:
        model = MediaFile
        fields = ['pk', 'title', 'fileType', 'file', 'thumbnail', 'createDate', 'updateDate', 'isDeleted']

    def get_file(self, obj):
        return reverse('image-resize', kwargs={'uuid': obj.pk})


class MediaPositionSerializer(CommonSerializer):
    class Meta:
        model = MediaPosition
        fields = '__all__'
        read_only_fields = ['slug']
