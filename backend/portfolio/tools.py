import os
import tempfile
import logging
from subprocess import call

logger = logging.getLogger(__name__)

def create_thumbnail_from_video(file):
    try:
        video_url = file.path
        logger.info(f"Generating thumbnail for video: {video_url}")

        video_path = video_url
        thumbnail_path = os.path.splitext(video_path)[0] + '_thumbnail.webp'

        result = call([
            'ffmpeg',
            '-i', video_path,
            '-ss', '00:00:01.000',
            '-vframes', '1',
            '-loglevel', 'quiet',
            '-hide_banner',
            thumbnail_path
        ])

        if result == 0 and os.path.exists(thumbnail_path):
            logger.info(f"Thumbnail successfully created at {thumbnail_path}")
            return thumbnail_path
        else:
            logger.warning(f"Thumbnail generation failed for video {video_url} with result: {result}")
            return None

    except Exception as e:
        logger.error(f"An error occurred while generating the thumbnail for video {video_url}: {e}")
        return None
