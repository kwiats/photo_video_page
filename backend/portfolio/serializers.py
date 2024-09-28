from django.urls import reverse
from rest_framework import serializers

from portfolio.models import MediaFile


class MediaFileSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = MediaFile
        fields = ['pk', 'title', 'file_type', 'file', 'create_date', 'update_date', 'is_deleted']

    def get_file(self, obj):
        return reverse('image-resize', kwargs={'uuid': obj.pk})