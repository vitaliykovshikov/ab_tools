from django.core.cache import cache
from django import http

def clean_cache_key(request, key):
    if request.user.is_authenticated() and request.user.is_superuser:
        cache.delete(key)
        return http.HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    raise http.Http404