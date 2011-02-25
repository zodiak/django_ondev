from django.core.management.base import NoArgsCommand, CommandError
from django.db.models import get_apps
from django.conf import settings
import os, os.path as osp
import shutil

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)

class Command(NoArgsCommand):
    help = "Compies media from all apps into MEDIA_ROOT."

    def handle_noargs(self, **options):
        if not osp.exists(MEDIA_ROOT):
            os.mkdir(MEDIA_ROOT)
        
        apps = get_apps()
        for x in apps:
            app_dir = osp.dirname(x.__file__)
            module = x.__name__
            app = module.split('.')[-2]

            media_dir = osp.join(app_dir, "media", app)
            if not osp.isdir(media_dir):
                media_dir = osp.join(app_dir, "media")
            if osp.exists(media_dir):
                print "copy", media_dir, '->', osp.join(MEDIA_ROOT, app)
                shutil.rmtree(osp.join(MEDIA_ROOT, app), True)
                shutil.copytree(media_dir, osp.join(MEDIA_ROOT, app))