import logging
import os
import ffmpeg
import time
from pathlib import Path
from django.core.files.base import ContentFile


logger = logging.getLogger(__name__)


def compress_video(file_video: str, resolution: str = None, quality: int = None, instance=None) -> ContentFile:
    if not os.path.isfile(file_video):
        logger.error(f"File {file_video} not found.")
        raise FileNotFoundError(f"File {file_video} not found.")

    if instance is None or not hasattr(instance, 'pk'):
        logger.error(f"Instance must be provided with a valid 'pk' attribute.")
        raise ValueError("Instance must be provided with a valid 'pk' attribute.")

    file_name = os.path.basename(file_video)
    output_dir = os.path.join('media', str(instance.pk))
    output_file = os.path.join(output_dir, f"compressed_{file_name}")

    os.makedirs(output_dir, exist_ok=True)

    logger.info(f"Starting compression for file: {file_video}")

    ffmpeg_input = ffmpeg.input(file_video)
    ffmpeg_args = {'preset': 'slower', 'threads': '4'}

    if quality:
        logger.info(f"Reducing quality to level: {quality}")
        ffmpeg_args['crf'] = str(quality)

    try:
        start_time = time.time()

        if resolution:
            logger.info(f"Changing resolution to: {resolution}")
            ffmpeg_output = ffmpeg_input.filter('scale', resolution).output(output_file, **ffmpeg_args)
        else:
            ffmpeg_output = ffmpeg_input.output(output_file, **ffmpeg_args)

        out, err = ffmpeg_output.run(capture_stdout=True, capture_stderr=True)

        log_ffmpeg_output(err.decode())

        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Compression completed in {duration:.2f} seconds. New file saved at: {output_file}")

        with open(output_file, 'rb') as f:
            file_data = f.read()

        return ContentFile(file_data, name=f"compressed_{file_name}")

    except ffmpeg.Error as e:
        logger.error(f"Compression error: {e.stderr.decode()}")
        raise


def log_ffmpeg_output(ffmpeg_log: str):
    important_lines = []
    for line in ffmpeg_log.splitlines():
        if "warning" in line.lower() or "error" in line.lower():
            important_lines.append(line.strip())

    if important_lines:
        logger.warning("FFmpeg warnings/errors during compression:\n" + "\n".join(important_lines))
    else:
        logger.info("FFmpeg finished without significant warnings or errors.")