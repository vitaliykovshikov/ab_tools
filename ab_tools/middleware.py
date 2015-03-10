#encoding: utf-8
import auth
import django
from django.utils.functional import SimpleLazyObject

OLD_DJANGO = False
if django.VERSION == (1, 3, 7, 'final', 0):
    OLD_DJANGO = True


#for old django
class LazyUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user'):
            request._cached_user = auth.get_user(request)
        return request._cached_user


def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user


class AuthenticationMiddleware(object):

    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        if OLD_DJANGO:
            request.__class__.user = LazyUser()
        else:
            request.user = SimpleLazyObject(lambda: get_user(request))