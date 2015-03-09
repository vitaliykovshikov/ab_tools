#encoding: utf-8

from datetime import datetime

from django.conf import settings
from django.contrib.sessions.backends.cached_db import SessionStore as CachedDbStore, KEY_PREFIX

try:
    from django.core.cache import caches
    django_version = '1.7'
except ImportError:
    from django.core.cache import get_cache
    django_version = '1.3'


class SessionStore(CachedDbStore):

    def __init__(self, session_key=None):
        if django_version == '1.3':
            self._cache = get_cache(settings.SESSION_CACHE_ALIAS)
        else:
            self._cache = caches[settings.SESSION_CACHE_ALIAS]
        super(SessionStore, self).__init__(session_key)

    def load(self):
        data = self._cache.get(KEY_PREFIX + self.session_key, None)
        expiry = data.get('_session_expiry') if data else None
        if data is None or (isinstance(expiry, datetime) and expiry < datetime.now()):
            data = super(CachedDbStore, self).load()
            self._cache.set(KEY_PREFIX + self.session_key, data,
                      settings.SESSION_COOKIE_AGE)
        return data

    def save(self, must_create=False):
        super(SessionStore, self).save(must_create)
        self._cache.set(KEY_PREFIX + self.session_key, self._session,
                  settings.SESSION_COOKIE_AGE)

    def delete(self, session_key=None):
        super(SessionStore, self).delete(session_key)
        self._cache.delete(KEY_PREFIX + (session_key or self.session_key))
