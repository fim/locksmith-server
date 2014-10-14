from django.conf.urls import patterns, include, url
from django.contrib import admin
from jsonrpc import jsonrpc_site

import locksmith.core.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'locksmith.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^json/$', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/', locksmith.core.views.autoregister,
        name="core_autoregister"),
)
