#encoding:utf-8
from haystack import connections as haystack_connections

from django.contrib.contenttypes.models import ContentType
try:
    from celery.decorators import task
except ImportError:
    from celery import task

@task(queue='elasticsearch.update_task')
def update_advert_task(object_pk, content_type_pk):
    instance = ContentType.objects.get(pk=content_type_pk).get_object_for_this_type(pk=object_pk)
    unified_index = haystack_connections['default'].get_unified_index()
    index = unified_index.get_index(instance)
    index.update_object(instance)
