# -*- coding: utf-8 -*-

from bson.son import SON
from mongoengine.queryset import QuerySet

from django.conf import settings

class ABMongoQuerySet(QuerySet):

    def geoNear(self, command, position, spherical=True, limit=None,
                maxDistance=None):
        obj_fields = ('_collection_obj', '_query', )
        obj_data = {}
        for field in obj_fields:
            field_data = getattr(self, field, None)
            if field_data is None:
                raise ValueError('There is no attr %s' % field)
            obj_data[field] = field_data

        if not isinstance(position, (list, tuple)):
            raise ValueError('position must be list or tuple')

        if limit is None:
            limit = self.count()

        db = settings.MONGODB
        query_settings = [
                ('geoNear', obj_data['_collection_obj'].name),
                (command, position),
                ('spherical', spherical),
                ('num', limit),
                ('query', obj_data['_query'])
            ]

        if maxDistance and isinstance(maxDistance, float):
            query_settings.append(
                (
                    'maxDistance',
                    maxDistance / float(settings.EARTH_RADIUS)
                )
            )

        query = SON(
            query_settings
        )

        result = db.command(query)

        return result['results']
