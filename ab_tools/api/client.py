#encoding: utf-8
import hashlib
import requests
from urlparse import urljoin

from django.conf import settings
from django.utils.translation import get_language
from django.core.cache import cache

import settings as api_settings



class AbApiClient(object):

    client = requests
    root_url = api_settings.AB_API_ROOT
    auth = api_settings.AB_API_AUTH

    def make_url(self, resource):
        lang = ''
        if not settings.LANGUAGE_CODE == get_language():
            lang = get_language()
            root_url = self.root_url % (lang + '/')
        else:
            root_url = self.root_url % lang
        return urljoin(root_url, resource)

    def get(self, resource, payload={}, cached=False, cached_time=60*15):
        url = self.make_url(resource)
        if cached:
            cache_key = hashlib.sha1(url + str(payload) + get_language()).hexdigest()
            response = cache.get(cache_key)
            if not hasattr(response, 'status_code'):
                response = self.client.get(url, params=payload, auth=self.auth)
                cache.set(cache_key, response, cached_time)
            return response
        return self.client.get(url, params=payload, auth=self.auth)

    def post(self, resource, payload={}):
        return self.client.post(self.make_url(resource), data=payload, auth=self.auth)
