from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from jsonrpc import jsonrpc_method

from django.core.urlresolvers import reverse_lazy
from django.core import serializers

# Create your views here.
from locksmith.core.models import Lock
import socket
import json

# Locks
class LockList(ListView):
    model = Lock

class LockCreate(CreateView):
    model = Lock
    success_url = reverse_lazy('privatekey_list')

class LockDelete(DeleteView):
    model = Lock
    success_url = reverse_lazy('privatekey_list')

class LockDetail(DetailView):
    model = Lock

# RPC calls
@jsonrpc_method('locksmith.lock', authenticated=True)
def lock(request, lock_name, exclusive=False):
    try:
        l = Lock.objects.get(stub=lock_name)
        l.lock(user=request.user, exclusive=exclusive)
    except Lock.DoesNotExist:
        l = Lock(stub=lock_name, locked=True, owner = request.user,
                multilock= not exclusive)
        l.save()

    return serializers.serialize('json', [ l ], fields=('locked', 'stub',
        'expire'))

@jsonrpc_method('locksmith.unlock', authenticated=True)
def unlock(request, lock_name):
    l = Lock.objects.get(stub=lock_name)
    l.unlock(user=request.user)
    return serializers.serialize('json', [ l ], fields=('locked', 'stub',
        'expire'))

@jsonrpc_method('locksmith.list', authenticated=True)
def list(request):
    l = Lock.objects.filter(owner=request.user)
    return serializers.serialize('json',  l, fields=('locked', 'stub',
        'expire'))

def autoregister(request):
    import socket
    if hasattr(socket, 'setdefaulttimeout'):
        socket.setdefaulttimeout(5)

    try:
        name = socket.gethostbyaddr(request.META['REMOTE_ADDR'])[0]
    except (Exception,e):
        name = request.META['REMOTE_ADDR']

    try:
        User.objects.get(username=name)
    except User.DoesNotExist:
        u = User(username=name)
        p = User.objects.make_random_password()
        u.set_password(p)
        u.save()
    else:
        return HttpResponse(status=400)

    return HttpResponse(json.dumps({ 'username': name, 'password': p}),
            content_type="application/json")
