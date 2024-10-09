def content_file_name(instance, filename):
    return '/'.join(['content', str(instance.pk), filename])