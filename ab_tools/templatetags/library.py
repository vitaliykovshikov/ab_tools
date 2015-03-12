#encoding: utf-8
from jinja2 import Markup
from jinja2 import contextfunction
from django_jinja import library

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import connections


@library.global_function
def cache_control_tool(user, fragment_name, args, **kwargs):
    """
    Template tag render button to reset block cache. For authenticated superuser.

    Usage: Jinja2
    1. Add 'ab_tools' to INSTALLED_APPS
    2. Add  url(r'^ab_tools/', include('ab_tools.urls')), to urls.py

    3. Use in templates
    {% set fragment_name='my_fragment_name' %}
    {% set cache_arguments=[arg1, arg2, arg3,...] %}
    {{ cache_control_tool(request.user, fragment_name, cache_arguments)}}

    {% cache 60*15 fragment_name cache_arguments %}
        ...
    {% endcache %}


    Will render link for delete cache for this block
    :param user: django.contrib.auth.models.User
    :param fragment_name: fragment name
    :param args: list of args
    :param kwargs:
    :return: html with button to delete cache key
    """
    if user and user.is_authenticated() and user.is_superuser:
        cache_key = make_template_fragment_key(fragment_name, args)
        return Markup(u'<a href="/ab_tools/cache/clean/%s/" class="btn btn-default">Обновить кеш</a>' % cache_key)
    return ''


@library.global_function
def get_make_model_rating(make):
    cache_key = 'rating_of:%s' % make
    rating = cache.get(cache_key)
    if not rating:
        cursor = connections['classifier'].cursor()
        cursor.execute("SELECT general_mark FROM reviews_carcomment WHERE make_id = %s AND publish = True" % make)
        marks = cursor.fetchall()
        if marks:
            rating = round(sum([m[0] for m in marks])/float(len(marks)), 1)
        else:
            rating = 0
        cache.set(cache_key, rating, 60*60*24)
    return rating
