#encoding: utf-8
from django.contrib.contenttypes.models import ContentType
from tasks import update_advert_task


def instance_update_search_index(sender, instance, **kwargs):
    update_advert_task.delay(instance.pk, ContentType.objects.get_for_model(instance.__class__))