# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from admin_tools.menu import items, Menu

# to activate your custom menu add the following to your settings.py:
#
# ADMIN_TOOLS_MENU = 'ondev.menu.CustomMenu'

class CustomMenu(Menu):
    """
    Custom Menu for ondev admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children.append(items.MenuItem(
            title=_('site'),
            url='/'
        ))
        self.children.append(items.MenuItem(
            title=_('Dashboard'),
            url=reverse('admin:index')
        ))
        self.children.append(items.MenuItem(
            title=u'Резервные копии',
            url=reverse('django_backup:index')
        ))
        self.children.append(items.MenuItem(
            title=u'Менеджер файлов',
            url=reverse('django_commander:index')
        ))
        self.children.append(items.MenuItem(
            title=u'Менеджер моделей',
            #url=reverse('admin:index')
        ))



    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass
