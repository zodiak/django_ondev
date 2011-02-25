from django.shortcuts import render_to_response, Http404, HttpResponseRedirect
from django.template.context import RequestContext
from django.core.management import call_command
from django.core.management.commands import dumpdata
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views import static
from os import listdir, path, remove, stat
from datetime import datetime
import tarfile


BACKUP_STORAGE = getattr(settings, 'BACKUP_STORAGE')
BACKUP_ROOT = getattr(settings, 'BACKUP_ROOT')

if not (BACKUP_STORAGE and BACKUP_ROOT):
    raise Exception('You should set BACKUP_STORAGE and BACKUP_ROOT constants in your settings')

def is_backup(filename):
    tarname = path.join(BACKUP_STORAGE, filename)
    return path.isfile(tarname) and filename.endswith('.tar.bz2') and tarfile.is_tarfile(tarname)

def get_size(filename):
    return stat(path.join(BACKUP_STORAGE, filename)).st_size
        
def index(request):
    content = listdir(BACKUP_STORAGE)
    backups = list([(item, get_size(item)) for item in content if is_backup(item)])
    backups.sort()
    context = {'backups': backups}
    return render_to_response('django_backup/index.html', context,
                                  context_instance = RequestContext(request))

def backup(request):
    if request.method != 'POST':
        raise Http404
    arcname = datetime.now().strftime("backup_%Y-%m-%d_%H-%M")
    tarname = arcname + '.tar.bz2'
    jsoname = arcname + '.json'
    
    #TODO: make list of files
    
    json = open(path.join(BACKUP_ROOT,jsoname),'w')
    json.write(dumpdata.Command().handle(**{'indent':4}))
    json.close()
    
    nameinarc = path.split(BACKUP_ROOT)[1]
    
    tar = tarfile.open(path.join(BACKUP_STORAGE,tarname), "w|bz2")
    tar.add(BACKUP_ROOT, nameinarc)
    tar.close()
    
    remove(path.join(BACKUP_ROOT,jsoname))
    
    return HttpResponseRedirect(reverse('django_backup:index'))

    

def restore(request):
    if request.method != 'POST':
        raise Http404
    try:
        arcname = request.POST.get('target')
        tarname = path.join(BACKUP_STORAGE, arcname)
        jsoname = path.join(BACKUP_ROOT, arcname.replace('.tar.bz2','.json'))
    except:
        raise Http404
    if path.exists(tarname) and is_backup(tarname):
        tar = tarfile.open(tarname)
        tar.extractall(path.join(BACKUP_ROOT,'..'))
        tar.close()
        
        call_command('cleardb',interactive=False)
        call_command('syncdb',interactive=False)
        try:
            call_command('migrate',interactive=False)
        except:
            pass
        call_command('loaddata',jsoname)
        
        remove(jsoname)
    else:
        raise Exception('Invalid backup: %s' % (arcname,))
    return HttpResponseRedirect(reverse('django_backup:index'))

def delete(request):
    if request.method != 'POST':
        raise Http404
    try:
        file = request.POST.get('target')
        remove(path.join(BACKUP_STORAGE,file))
    except:
        raise Http404
    return HttpResponseRedirect(reverse('django_backup:index'))

def delete_selected(request):
    if request.method != 'POST':
        raise Http404
    try:
        files = request.POST['selected_action']
        #remove(path.join(BACKUP_STORAGE,file))
    except:
        raise Http404
    return HttpResponseRedirect(reverse('django_backup:index'))

def download(request, file):
    return static.serve(request, file, BACKUP_STORAGE, False)
