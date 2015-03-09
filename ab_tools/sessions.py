#encoding: utf-8

from datetime import datetime

from django.conf import settings
from django.contrib.sessions.backends.cached_db import SessionStore as CachedDbStore, KEY_PREFIX
from django.core.cache import cache


class SessionStore(CachedDbStore):

    def load(self):
        data = cache.get(KEY_PREFIX + self.session_key, None)
        expiry = data.get('_session_expiry') if data else None
        if data is None or (isinstance(expiry, datetime) and expiry < datetime.now()):
            data = super(CachedDbStore, self).load()
            cache.set(KEY_PREFIX + self.session_key, data,
                      settings.SESSION_COOKIE_AGE)
        return data