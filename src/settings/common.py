import sys
from os import path

PROJECT_DIR = path.abspath(path.join(path.dirname(__file__), '..'))

# need to think how to use cache...
# CACHE_BACKEND = 'locmem:///'

ADMINS = (
    ('Zodiak', 'DesZodiak@gmail.com'),
)
MANAGERS = ADMINS

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_URL = '/media/'
MEDIA_ROOT = path.join(PROJECT_DIR, 'media')

STATIC_URL = '/media/static/'
STATIC_ROOT = path.join(MEDIA_ROOT, 'static')

ADMIN_MEDIA_PREFIX = '/media/static/admin/'
ADMIN_TOOLS_MEDIA_URL = MEDIA_URL

STATICFILES_FINDERS = (
   #'staticfiles.finders.FileSystemFinder', 
   'staticfiles.finders.AppDirectoriesFinder',
   'django_mediacompressor.finders.LegacyAppDirectoriesFinder',
   #'staticfiles.finders.DefaultStorageFinder',
)


APPEND_SLASH = True

SECRET_KEY = '*#hb5d+_ml%f*4)bby((ka#2b-!h7m0ng(chx6tb@c(l&z+55f'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS =(
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'cms.context_processors.media',
    'django.core.context_processors.request',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # i don't use multilangual in this way
    # 'cms.middleware.multilingual.MultilingualURLMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cms.middleware.media.PlaceholderMediaMiddleware', 
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'sentry.client.middleware.Sentry404CatchMiddleware',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    # django-admin-tools app
    'admin_tools', # need to collect media files
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    # django default apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    
    # django-cms apps
    'cms',
    'publisher',
    'menus',
    'mptt',
    
    # django-cms standard plugins
    'cms.plugins.text',
    'cms.plugins.picture',
    'cms.plugins.file',
    'cms.plugins.flash',
    'cms.plugins.link',
    'cms.plugins.snippet',
    'cms.plugins.googlemap',
    'cms.plugins.teaser',
    'cms.plugins.video',
    'cms.plugins.twitter',
    'cms.plugins.inherit',
    
    'easy_thumbnails',    
    
    'south',
    
    # django-sentry app
    'indexer',
    'paging',
    'sentry',
    'sentry.client',
    
    # dont know who needs it
    # 'appmedia',
    
    'staticfiles',

    # need to collect media from this project
    'project',

    # my own apps to improove cms
    # to use command 'compressmedia'
    'django_mediacompressor',
    #'admin_tools_fix',
    'django_backup',
    'django_commander',
)


BACKUP_STORAGE = path.join(PROJECT_DIR, 'backups')
BACKUP_ROOT = PROJECT_DIR

ADMIN_TOOLS_MEDIA_URL = '/media/static/'
ADMIN_TOOLS_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'dashboard.CustomAppIndexDashboard'
ADMIN_TOOLS_MENU = 'menu.CustomMenu'



# django-cms settings
CMS_MEDIA_URL = '/media/static/cms/'

gettext = lambda s: s

LANGUAGE_CODE = 'ru-RU'

LANGUAGES = (
    ('ru', gettext('Russian')),
)

CMS_TEMPLATES = (
    ('col_two.html', gettext('two columns')),
    ('col_three.html', gettext('three columns')),
    ('nav_playground.html', gettext('navigation examples')),
)

CMS_SOFTROOT = True
CMS_MODERATOR = True
CMS_PERMISSION = True
CMS_REDIRECTS = True
CMS_SEO_FIELDS = True
CMS_FLAT_URLS = False
CMS_MENU_TITLE_OVERWRITE = True
CMS_HIDE_UNTRANSLATED = False
CMS_URL_OVERWRITE = True

try:
    from local_settings import *
except ImportError:
    pass