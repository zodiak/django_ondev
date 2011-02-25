# -*- coding: utf-8 -*-
from __future__ import with_statement
from django.shortcuts import render_to_response, Http404
from django.template.context import RequestContext
from django_commander.commander import dir_index, ROOT
from os import path
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter


def index(request):
    context = {}
    return render_to_response('django_commander/index.html',context,
                              context_instance = RequestContext(request))
    
def panel(request):
    if request.method=="GET":
        pth = request.GET.get('path', '')
        valid, items = dir_index(pth)
        if not valid:
            return Http404
        context = {'items': items,
                   'path': pth}
        return render_to_response('django_commander/panel.html',context,
                                  context_instance = RequestContext(request))
    else:
        raise Http404    

def view(request, filename):
    content = ''
    with open(path.join(ROOT,filename)) as f:
        for line in f:
            content += line.decode('utf-8')
    lexer = get_lexer_for_filename(filename)
    formatter = HtmlFormatter()
    html = highlight(content, lexer, formatter)
    css = formatter.get_style_defs('.highlight')
    context = {'css': css, 'html': html, 'filename': filename}
    return render_to_response('django_commander/view.html',context,
                              context_instance = RequestContext(request))

def edit(request, filename):
    context = {}
    return render_to_response('django_commander/edit.html',context,
                              context_instance = RequestContext(request))