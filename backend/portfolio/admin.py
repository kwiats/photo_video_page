# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin

from portfolio.models import MediaFile, MediaPosition,ProcessedMediaFile



@admin.register(MediaPosition)
class MediaPositionAdmin(SimpleHistoryAdmin):
    list_display = (
        'uuid',
        'update_date',
        'name',

    )
    list_filter = ('is_deleted', 'update_date')
    search_fields = ('name', 'uuid')


@admin.register(ProcessedMediaFile)
class ProcessedMediaFileAdmin(SimpleHistoryAdmin):
    list_display = (
        'uuid',
        'update_date',
        'status',
        'resolution',
        'quality',
    )
    list_filter = ('is_deleted', 'update_date')
    search_fields = 'uuid'


@admin.register(MediaFile)
class MediaFileAdmin(SimpleHistoryAdmin):
    list_display = (
        'uuid',
        'update_date',
        'title',
        'file_type',
        'is_public',
        'file',
        'public_url',
        'image_img'
    )
    list_filter = ('is_deleted', 'update_date')
    search_fields = ('title', 'file_type', 'uuid')

    def public_url(self, obj):
        return format_html('<a href="{}" target="_blank">Public URL</a>',
                           reverse('image-resize', kwargs={'uuid': obj.pk}))

    def image_img(self, obj):
        if obj.file_type == 'image':
            return format_html('<img src="{}" style="width: 250px; height: auto;" />', obj.file.url)
        elif obj.file_type == 'video':
            return format_html(
                '<video width="250" autoplay muted loop>'
                '<source src="{}" type="video/mp4">'
                'Your browser does not support the video tag.'
                '</video>',
                obj.file.url
            )
        else:
            return '(No preview available)'

    image_img.short_description = 'Miniaturka'
    public_url.short_description = 'Publiczny url'
