import logging
import os.path
from os.path import basename
from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from censo.models import Cliente
log = logging.getLogger(__name__)





def descargar_apk(request):
    """
    Vista para servir el APK
    :param request:
    :return:
    """
    mime = 'application/vnd.android.package-archive'

    filename = os.path.join(settings.APK_FILE_STORAGE_PATH, 'censo.apk')

    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper)
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Type'] = mime
    response['Content-Disposition'] = 'inline; filename=%s' % basename(filename)
    return response

def map_view(request):
    clientes = Cliente.objects.all()
    return render_to_response('map.html', {'clientes': clientes}, context_instance=RequestContext(request))



def crear_ruta(request):
    """
    Vista para crear rutas
    :param request:
    :return:
    """
    pass
