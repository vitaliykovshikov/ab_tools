#encoding: utf-8
from django.conf import settings

AB_API_ROOT = getattr(settings, 'AB_API_ROOT', 'http://avtobazar.ua/api/v2/')

AB_API_LOGIN = getattr(settings, 'AB_API_LOGIN', '')
AB_API_PASSWORD = getattr(settings, 'AB_API_PASSWORD', '')

AB_API_AUTH = (AB_API_LOGIN, AB_API_PASSWORD)