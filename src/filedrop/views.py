from datetime import datetime, date, time, timedelta
from django.db.models import Count
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.shortcuts import render_to_response, redirect, get_object_or_404, get_list_or_404
from django.template import Context, loader
from django.views.decorators.cache import cache_control, never_cache
from filedrop.models import Message, File
import logging

def _get_message(request, key):
    msg = get_object_or_404(Message, key=key)
    if msg.require_authentication:
        if not request.user.is_authenticated():
            return HttpResonseRedirect('/%s/?%s=%s' % ('accounts/login', 'next', request.path))
        elif request.user not in msg.recipients and not request.user.is_superuser:
            return HttpResponseForbidden()
    return msg

def home(request):
    raise NotImplementedError

def dropoff(request, key=None):
    if key is None:
        # Creating a new dropoff
        msg = Message()
        # TODO: Parse form
        raise NotImplementedError
    else:
        # Updating an existing dropoff
        raise NotImplementedError

def upload(request, key=None):
    if key is None:
        # General Upload
        raise NotImplementedError
    else:
        # Dropoff Upload
        raise NotImplementedError

def pickup(request, key=None):
    raise NotImplementedError

def download(request, key=None, file_id=None, filename=None):
    msg = _get_message(request, key)
    file_ = get_object_or_404(File, message__pk=msg.pkg, pk=file_id)
    
    if settings.get('USE_XSENDFILE', False):
        response = HttpResponse(mimetype=file_.mimetype)
        # response['Content-Type'] = file_.mimetype
        response['Content-Length'] = file_.size
        response['X-Sendfile'] = file_.path
    else:
        f = file_.data.storage
        f.open('rb+')
        try:
            response = HttpResponse(file_.chunks(), mimetype=file_.mimetype)
        finally:
            f.close()
        # response['Content-Length'] = file_.size
    
    # Force the download screen
    # response['Content-Disposition'] = 'attachment; filename="' + file_.filename + '"'
    return response

