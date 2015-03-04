#encoding: utf-8
from django.conf.urls import patterns, url

from views import clean_cache_key

urlpatterns = patterns('',
    url(r'^cache/clean/(?P<key>.*)/$', clean_cache_key, name='ab_tools_clean_cache_key'),
)