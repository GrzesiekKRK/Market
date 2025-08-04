from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """
    Storage class for static files (CSS, JS, images used in templates)
    """
    location = settings.STATIC_LOCATION
    default_acl = 'public-read'
    file_overwrite = True


class MediaStorage(S3Boto3Storage):
    """
    Storage class for user uploaded media files (public access)
    """
    location = ''
    default_acl = 'public-read'
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    """
    Storage class for private media files (restricted access)
    """
    location = settings.PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False  # Don't use CDN for private files
