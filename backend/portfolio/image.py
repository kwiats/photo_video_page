from io import BytesIO
from typing import Optional, Tuple

from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile


def process_image(image_file: str, resolution: Optional[Tuple[int, int]] = None,
                  quality: int = 75) -> ContentFile:
    img = Image.open(image_file)

    if img.mode == 'RGBA':
        img = img.convert('RGB')

    if resolution:
        img = img.resize(resolution, Image.Resampling.LANCZOS)

    output = BytesIO()
    img.save(output, format='WEBP', quality=quality)
    output.seek(0)

    new_filename = image_file.name.rsplit('.', 1)[0] + '.webp'
    return ContentFile(output.read(), name=new_filename)