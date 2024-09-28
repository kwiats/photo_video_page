from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile


def process_image(image_file, resolution=None, quality=75):
    img = Image.open(image_file)
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    if resolution:
        img = img.resize(resolution, Image.Resampling.LANCZOS)

    output = BytesIO()
    img.save(output, format='JPEG', quality=quality)
    output.seek(0)

    return ContentFile(output.read(), name=image_file.name)
