def content_file_name(instance, filename):
    return '/'.join(['content', instance.pk, filename])
