# -*- coding: utf-8 -*-
from django.conf import settings
import os, time
from os import path
from datetime import datetime

ROOT = getattr(settings, 'PROJECT_DIR', path.abspath(__file__))

class Item:
    def __init__(self, pth, up=False):
        self.isdir = path.isdir(pth)
        stat = os.stat(pth)
        self.url = path.relpath(path.abspath(pth), ROOT)
        self.url = '' if self.url == '.' else self.url
        
        self.path, self.fullname = path.split(pth)
        self.name, ext = path.splitext(self.fullname)
        self._ext = ext[1:] if ext.startswith('.') else ext
        self.name = '..' if up else self.name
        
        self.modified = datetime.fromtimestamp(stat.st_mtime)
        self.size = stat.st_size
        self.rights = '-rwxr-x---'
        
        self.target = True if (not self.isdir) and self.size > 1024 else False
        
    def type(self):
        return 'dir' if self.isdir else 'file'
    
    def ext(self):
        return 'dir' if self.isdir else self._ext

    def __cmp__(self, other):
        if type(other) != type(self):
            raise TypeError('Unable to compare %s to %s'%(type(self), type(other)))
        return cmp(other.isdir, self.isdir) or cmp(self.name, other.name)
            
def dir_index(pth):
    if pth.count('..') != 0:
        return False, []
    realpath = path.abspath(path.join(ROOT,pth))
    content = os.listdir(realpath)
    items = [Item(path.join(realpath,item)) for item in content]
    items.sort()
    if realpath != ROOT:
        items.insert(0, Item(path.join(realpath, '..'), True))
    return True, items
