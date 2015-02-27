#encoding: utf-8
import requests
from urlparse import urljoin

import settings as api_settings


class AbApiClient(object):

    client = requests
    root_url = api_settings.AB_API_ROOT
    auth = api_settings.AB_API_AUTH

    def make_url(self, resource):
        return urljoin(self.root_url, resource)

    def get(self, resource, payload={}):
        return self.client.get(self.make_url(resource), params=payload)

    def post(self, resource, payload={}):
        return self.client.post(self.make_url(resource), data=payload)


