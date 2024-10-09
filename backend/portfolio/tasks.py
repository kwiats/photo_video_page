import logging
import os
from uuid import UUID

from celery import shared_task

from portfolio.image import process_image
from portfolio.models import MediaFile, ProcessedMediaFile
from portfolio.tools import create_thumbnail_from_video
from portfolio.video import compress_video

logger = logging.getLogger(__name__)


@shared_task
def generate_thumbnail(media_file_id: UUID):
    logger.info(f"Generating thumbnail for MediaFile ID: {media_file_id}")

    try:
        media_file = MediaFile.objects.get(pk=media_file_id)
        if media_file.file_type == 'video':
            thumbnail_url = create_thumbnail_from_video(media_file.file)
            if thumbnail_url:
                media_file.thumbnail = thumbnail_url
                media_file.save()
                logger.info(f"Thumbnail successfully generated for MediaFile ID: {media_file_id}")
            else:
                logger.warning(f"Thumbnail generation failed for MediaFile ID: {media_file_id}")
            return thumbnail_url
    except MediaFile.DoesNotExist:
        logger.error(f"MediaFile with id {media_file_id} does not exist.")
        return None
    except Exception as e:
        logger.error(f"An error occurred while generating thumbnail for MediaFile ID: {media_file_id}: {e}")
        return None


@shared_task
def compress_video_task(media_file_id, resolution=None, quality=100):
    logger.info(
        f"Starting video compression for MediaFile ID: {media_file_id}, resolution: {resolution}, quality: {quality}")

    try:
        media_file = MediaFile.objects.prefetch_related('processedmediafile_set').get(pk=media_file_id)
    except MediaFile.DoesNotExist:
        logger.error(f"MediaFile with id {media_file_id} does not exist.")
        return

    if media_file.processedmediafile_set.filter(resolution=resolution, quality=quality).exists():
        logger.info(
            f"Processed video already exists for MediaFile ID: {media_file_id}, resolution: {resolution}, quality: {quality}")
        return

    processed_media_file = ProcessedMediaFile.objects.create(
        media_file=media_file,
        resolution=resolution,
        quality=quality,
        status='processing'
    )

    try:
        original_file_path = media_file.file.path

        if media_file.file_type == 'video':
            compressed_file = compress_video(original_file_path, resolution=resolution, quality=quality,
                                                  instance=media_file)
        else:
            compressed_file = process_image(media_file.file, resolution=resolution, quality=quality)

        processed_media_file.processed_file.save(compressed_file.name,
                                                 compressed_file)

        processed_media_file.status = 'ready'
        processed_media_file.save()

        logger.info(f"Video compression successful for MediaFile ID: {media_file_id}, saved as {compressed_file}")

    except Exception as e:
        processed_media_file.status = 'failed'
        processed_media_file.is_deleted = True
        processed_media_file.save()
        logger.error(f"Video compression failed for MediaFile ID: {media_file_id}, error: {e}")
        raise e
