from datetime import datetime
from django.conf import settings
from django.db import models

def statistic_for_object(object_variable=None, check_last_ip=False, obj_class=None):
    def decorator(func):
        def wrapper(request, *args, **kwargs):

            output = func(request, *args, **kwargs)

            obj = None
            skip_statistic = False
            if isinstance(output, dict):
                if object_variable and not obj_class in output and \
                   hasattr(output[object_variable], 'pk'):
                    obj = output[object_variable]
                    class_name = obj.__class__.__name__
                elif obj_class:
                    class_name = obj_class
                skip_statistic = output.get('skip_statistic', False)
            elif isinstance(output, models.Model):
                if output._meta.proxy == True:
                    obj = output
                    class_name = obj._meta.proxy_for_model.__name__
                else:
                    # TODO: implement this section, if necessary
                    pass

            if (obj or obj_class) and not skip_statistic:
                mongodb = settings.MONGODB
                date = datetime.now().date().toordinal()
                data = {
                    'date': date,
                    'class': class_name,
                    'pk': obj.pk if obj else output['pk']
                }
                if mongodb:
                    mongo_data = mongodb.statistics.find_one(data)
                    if not mongo_data:
                        data['count'] = 1
                        if check_last_ip:
                            data['last_ip'] = request.META.get('REMOTE_ADDR', '')
                        mongodb.statistics.insert(data)
                    else:
                        new_data = {'count': mongo_data['count'] + 1}

                        if check_last_ip:
                            last_ip = mongo_data.get('last_ip', None)
                            current_ip = request.META.get('REMOTE_ADDR', '')
                            if not last_ip is None:
                                if last_ip == current_ip:
                                    return output
                            new_data['last_ip'] = current_ip

                        mongodb.statistics.update(
                            {'_id': mongo_data['_id']},
                            {'$set': new_data}
                        )
            return output
        return wrapper
    return decorator
