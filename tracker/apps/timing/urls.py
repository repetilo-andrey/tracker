from django.conf.urls.defaults import patterns, url
from jsonrpc import jsonrpc_site

import rpc

urlpatterns = patterns('',
    url(r'^rpc/', jsonrpc_site.dispatch, name="jsonrpc_mountpoint"),
)
