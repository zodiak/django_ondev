import os
from django.conf import settings

FILER_SUBJECT_LOCATION_IMAGE_DEBUG = getattr(settings, 'FILER_SUBJECT_LOCATION_IMAGE_DEBUG', False)

FILER_IS_PUBLIC_DEFAULT = getattr(settings, 'FILER_IS_PUBLIC_DEFAULT', False)

FILER_STATICMEDIA_PREFIX = os.path.normpath( getattr(settings, 'FILER_STATICMEDIA_PREFIX', os.path.join(settings.MEDIA_URL,'filer/') ) ) + '/'

FILER_PUBLICMEDIA_PREFIX = os.path.normpath( getattr(settings, 'FILER_PUBLICMEDIA_PREFIX', 'filer_public') )
FILER_PRIVATEMEDIA_PREFIX = os.path.normpath( getattr(settings, 'FILER_PRIVATEMEDIA_PREFIX', 'filer_private') )

# please don't change these in settings for now. all media dirs must be beneath MEDIA_ROOT!
FILER_PUBLICMEDIA_URL = os.path.normpath( getattr(settings, 'FILER_PUBLICMEDIA_URL', os.path.join(settings.MEDIA_URL,FILER_PUBLICMEDIA_PREFIX) ) )
FILER_PUBLICMEDIA_ROOT = os.path.abspath( os.path.join(settings.MEDIA_ROOT, FILER_PUBLICMEDIA_PREFIX ) )

FILER_PRIVATEMEDIA_URL = os.path.normpath( getattr(settings, 'FILER_PRIVATEMEDIA_URL', os.path.join(settings.MEDIA_URL,FILER_PRIVATEMEDIA_PREFIX) ) )
FILER_PRIVATEMEDIA_ROOT = os.path.abspath( os.path.join(settings.MEDIA_ROOT, FILER_PRIVATEMEDIA_PREFIX ) )


FILER_ADMIN_ICON_SIZES = (
        '16', '32', '48', '64', 
)

# windows fix
FILER_STATICMEDIA_PREFIX = FILER_STATICMEDIA_PREFIX.replace(os.path.sep , '/')
FILER_PUBLICMEDIA_PREFIX = FILER_PUBLICMEDIA_PREFIX.replace(os.path.sep, '/')
FILER_PRIVATEMEDIA_PREFIX = FILER_PRIVATEMEDIA_PREFIX.replace(os.path.sep, '/')
FILER_PUBLICMEDIA_URL = FILER_PUBLICMEDIA_URL.replace(os.path.sep, '/')
FILER_PRIVATEMEDIA_URL = FILER_PRIVATEMEDIA_URL.replace(os.path.sep, '/')



"""
FILER_STATICMEDIA_PREFIX = getattr(
    settings, 
    'FILER_STATICMEDIA_URL', 
    settings.MEDIA_URL + 'filer/'
)

FILER_PUBLICMEDIA_PREFIX = getattr(
    settings, 
    'FILER_PUBLICMEDIA_PREFIX', 
    'filer_public'
)

FILER_PRIVATEMEDIA_PREFIX = getattr(
    settings, 
    'FILER_PRIVATEMEDIA_PREFIX', 
    'filer_private'
)

FILER_PUBLICMEDIA_URL = getattr(
    settings, 
    'FILER_PUBLICMEDIA_URL', 
    settings.MEDIA_URL + FILER_PUBLICMEDIA_PREFIX + '/'
)

FILER_PUBLICMEDIA_ROOT = getattr(
    settings,
    'FILER_PUBLICMEDIA_ROOT',
    os.path.join(settings.MEDIA_ROOT, FILER_PUBLICMEDIA_PREFIX)
)

FILER_PRIVATEMEDIA_URL = getattr(
    settings, 
    'FILER_PRIVATEMEDIA_URL', 
    settings.MEDIA_URL + FILER_PRIVATEMEDIA_PREFIX + '/'
)

FILER_PRIVATEMEDIA_ROOT = getattr(
    settings,
    'FILER_PRIVATEMEDIA_ROOT',
    os.path.join(settings.MEDIA_ROOT, FILER_PRIVATEMEDIA_PREFIX)
)
"""
