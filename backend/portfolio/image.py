from io import BytesIO
from typing import Optional, Tuple

from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile


def process_image(image_file, resolution: Optional[Tuple[int, int]] = None, quality: int = 75, output_path: str = None) -> str:
    img = Image.open(image_file.path)

    if img.mode == 'RGBA':
        img = img.convert('RGB')

    if resolution:
        img = img.resize(resolution, Image.Resampling.LANCZOS)

    if output_path is None:
        base_name = str(image_file.name).rsplit('.', 1)[0].replace(' ', '_')
        output_path = f"{base_name}.webp"

    img.save(output_path, format='WEBP', quality=quality)

    return output_path