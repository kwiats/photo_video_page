from django.conf import settings

from portfolio.tasks import compress_video_task, generate_thumbnail


def generate_thumbnail_runner(media_file_id):
    if settings.DEBUG:
        generate_thumbnail(media_file_id)
    else:
        generate_thumbnail.delay(media_file_id)


def compress_media_runner(media_file_id, resolution=None, quality=75):
    if settings.DEBUG:
        compress_video_task(media_file_id, resolution, quality)
    else:
        compress_video_task.delay(media_file_id, resolution, quality)
