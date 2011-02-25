from django.core.management.base import NoArgsCommand
from django.conf import settings
from os import walk, path
import subprocess
import django_mediacompressor

COMPRESSOR = path.join(path.dirname(django_mediacompressor.__file__),
                         'yuicompressor.jar')


class Command(NoArgsCommand):
    help = "Compress all JavaScript and CSS in MEDIA_ROOT."

    def handle_noargs(self, **options):
        MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)
        for file in self.find_media(MEDIA_ROOT):
            print file
            self.compress(file)

    def find_media(self, root_dir):
        for root, dirs, files in walk(root_dir):
            for file in files:
                if self.compressable(file):
                    yield path.join(root, file)
                
    def compressable(self, file):
        ext = path.splitext(file)
        ext = ext[1] or ext[0]
        if ext == '':
            return False
        return True if ext in ['.js', '.css'] else False

    def compress(self, file):
        ext = path.splitext(file)[1]
        if ext == '.js':
            subprocess.Popen(['java', '-jar', COMPRESSOR, '--type', 'js',
                              file, '-o', file]).wait()
        if ext == '.css':
            subprocess.Popen(['java', '-jar', COMPRESSOR, '--type', 'css',
                              file, '-o', file]).wait()
                    