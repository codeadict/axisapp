from django_jinja import library
from django.conf import settings
from django.core.files.storage import get_storage_class
media_storage = get_storage_class()()


@library.global_function
def media(file_name):
    return media_storage.url(unicode(file_name))