import os
import fnmatch
import warnings
from inspect import getmembers

from django.conf import settings

def get_files_for_app(app, ignore_patterns=[]):
    """
    Return a list containing the relative source paths for all files that
    should be copied for an app.
    
    """
    from staticfiles.storage import AppStaticStorage
    warnings.warn(
        "The staticfiles.utils.get_files_for_app utility function is "
        "deprecated. Use staticfiles.storage.AppStaticStorage.get_files "
        "instead.", PendingDeprecationWarning)
    return AppStaticStorage(app).get_files(ignore_patterns)

def get_app_prefix(app):
    """
    Return the path name that should be prepended to files for this app.
    """
    from staticfiles.storage import AppStaticStorage
    warnings.warn(
        "The staticfiles.utils.get_app_prefix utility function is "
        "deprecated. Use staticfiles.storage.AppStaticStorage.get_prefix "
        "instead.", PendingDeprecationWarning)
    return AppStaticStorage(app).get_prefix()

def is_ignored(path, ignore_patterns=[]):
    """
    Return True or False depending on whether the ``path`` should be
    ignored (if it matches any pattern in ``ignore_patterns``).
    """
    for pattern in ignore_patterns:
        if fnmatch.fnmatchcase(path, pattern):
            return True
    return False

def get_files(storage, ignore_patterns=[], location=''):
    """
    Recursively walk the storage directories yielding the paths
    of all files that should be copied.
    """
    directories, files = storage.listdir(location)
    for fn in files:
        if is_ignored(fn, ignore_patterns):
            continue
        if location:
            fn = os.path.join(location, fn)
        yield fn
    for dir in directories:
        if is_ignored(dir, ignore_patterns):
            continue
        if location:
            dir = os.path.join(location, dir)
        for fn in get_files(storage, ignore_patterns, dir):
            yield fn


class AppSettings(object):
    """
    An app setting object to be used for handling app setting defaults
    gracefully and providing a nice API for them. Say you have an app
    called ``myapp`` and want to define a few defaults, and refer to the
    defaults easily in the apps code. Add a ``settings.py`` to your app::

        from path.to.utils import AppSettings

        class MyAppSettings(AppSettings):
            SETTING_1 = "one"
            SETTING_2 = (
                "two",
            )

    Then initialize the setting with the correct prefix in the location of
    of your choice, e.g. ``conf.py`` of the app module::

        settings = MyAppSettings(prefix="MYAPP")

    The ``MyAppSettings`` instance will automatically look at Django's
    global setting to determine each of the settings and respect the
    provided ``prefix``. E.g. adding this to your site's ``settings.py``
    will set the ``SETTING_1`` setting accordingly::

        MYAPP_SETTING_1 = "uno"

    Usage
    -----

    Instead of using ``from django.conf import settings`` as you would
    usually do, you can switch to using your apps own settings module
    to access the app settings::

        from myapp.conf import settings

        print myapp_settings.MYAPP_SETTING_1

    ``AppSettings`` instances also work as pass-throughs for other
    global settings that aren't related to the app. For example the
    following code is perfectly valid::

        from myapp.conf import settings

        if "myapp" in settings.INSTALLED_APPS:
            print "yay, myapp is installed!"

    Custom handling
    ---------------

    Each of the settings can be individually configured with callbacks.
    For example, in case a value of a setting depends on other settings
    or other dependencies. The following example sets one setting to a
    different value depending on a global setting::

        from django.conf import settings

        class MyCustomAppSettings(AppSettings):
            ENABLED = True

            def configure_enabled(self, value):
                return value and not self.DEBUG

        custom_settings = MyCustomAppSettings("MYAPP")

    The value of ``custom_settings.MYAPP_ENABLED`` will vary depending on the
    value of the global ``DEBUG`` setting.

    Each of the app settings can be customized by providing
    a method ``configure_<lower_setting_name>`` that takes the default
    value as defined in the class attributes as the only parameter.
    The method needs to return the value to be use for the setting in
    question.
    """
    def __dir__(self):
        return sorted(list(set(self.__dict__.keys() + dir(settings))))

    __members__ = lambda self: self.__dir__()

    def __getattr__(self, name):
        if name.startswith(self._prefix):
            raise AttributeError("%r object has no attribute %r" %
                                 (self.__class__.__name__, name))
        return getattr(settings, name)

    def __setattr__(self, name, value):
        super(AppSettings, self).__setattr__(name, value)
        if name in dir(settings):
            setattr(settings, name, value)

    def __init__(self, prefix):
        super(AppSettings, self).__setattr__('_prefix', prefix)
        for name, value in filter(self.issetting, getmembers(self.__class__)):
            prefixed_name = "%s_%s" % (prefix.upper(), name.upper())
            value = getattr(settings, prefixed_name, value)
            callback = getattr(self, "configure_%s" % name.lower(), None)
            if callable(callback):
                value = callback(value)
            delattr(self.__class__, name)
            setattr(self, prefixed_name, value)

    def issetting(self, (name, value)):
        return name == name.upper()