#encoding: utf-8
from jinja2 import Markup
from jinja2 import contextfunction
from django_jinja import library

from django.core.cache.utils import make_template_fragment_key


@library.global_function
def cache_control_tool(user, fragment_name, *args, **kwargs):
    if user and user.is_authenticated() and user.is_superuser:
        cache_key = make_template_fragment_key(fragment_name, args)
        return Markup(u'<a href="/ab_tools/cache/clean/%s/" class="btn btn-default">Обновить кеш</a>' % cache_key)
    return ''