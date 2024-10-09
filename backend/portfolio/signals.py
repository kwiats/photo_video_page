from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify

from portfolio.models import MediaFile, MediaPosition
from portfolio.task_runner import compress_media_runner, generate_thumbnail_runner


@receiver(pre_save, sender=MediaFile)
def set_title(sender, instance, **kwargs):
    if not instance.title:
        instance.title = instance.file.name


@receiver(post_save, sender=MediaFile)
def generate_video_thumbnail(sender, instance, created, **kwargs):
    if instance.file_type == 'video' and not instance.thumbnail:
        generate_thumbnail_runner(instance.pk)


@receiver(post_save, sender=MediaFile)
def compress_media(sender, instance, created, **kwargs):
    compress_media_runner(instance.pk)


@receiver(pre_save, sender=MediaPosition)
def create_unique_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.name)
        slug = base_slug
        counter = 1

        while MediaPosition.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        instance.slug = slug
