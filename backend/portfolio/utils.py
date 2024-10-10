def content_file_name(instance, filename):
    file_type = getattr(instance, 'file_type', None) or getattr(instance.media_file, 'file_type', 'unknown')

    instance_pk = str(instance.pk) if instance.pk else 'temp'

    return '/'.join([file_type, instance_pk, filename])