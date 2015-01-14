__author__ = 'codeadict'
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage

import storages.backends.s3boto


class StaticStorage(storages.backends.s3boto.S3BotoStorage):
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = settings.STATIC_AWS_STORAGE_BUCKET_NAME
        kwargs['headers'] = settings.STATIC_AWS_HEADERS
        kwargs['querystring_auth'] = settings.STATIC_AWS_QUERYSTRING_AUTH
        kwargs['acl'] = settings.STATIC_AWS_DEFAULT_ACL
        super(StaticStorage, self).__init__(*args, **kwargs)


class PublicStorage(storages.backends.s3boto.S3BotoStorage):
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = settings.PUBLIC_AWS_STORAGE_BUCKET_NAME
        kwargs['headers'] = settings.PUBLIC_AWS_HEADERS
        kwargs['querystring_auth'] = settings.PUBLIC_AWS_QUERYSTRING_AUTH
        kwargs['acl'] = settings.PUBLIC_AWS_DEFAULT_ACL
        super(PublicStorage, self).__init__(*args, **kwargs)


class PublicDebugStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None, **kwargs):
        tmp_loc = os.path.join(settings.MEDIA_ROOT, 'public/')
        tmp_url = settings.PUBLIC_URL
        super(PublicDebugStorage, self).__init__(location=tmp_loc, base_url=tmp_url, **kwargs)
