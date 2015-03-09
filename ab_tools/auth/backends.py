# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.backends import ModelBackend as DjangoModelBackend
from django.contrib.auth.models import User

from registration.models import RegistrationProfile

from documents import InactiveUser
from utils import activate_profile


def check_inactive(func):
    def wrapper(*args, **kwargs):
        user = func(*args, **kwargs)
        if not user is None and not user.is_active and settings.MONGODB:
            try:
                inactive = InactiveUser.objects.get(user=user.pk)
            except InactiveUser.DoesNotExist:
                pass
            else:
                profiles = list(user.registrationprofile_set.all())
                if profiles:
                    activated = activate_profile(profiles[0])
                    if not activated is None:
                        user = activated
                inactive.delete()
        return user
    return wrapper


class InactiveMixin(object):

    def __init__(self, *args, **kwargs):
        self.authenticate = check_inactive(self.authenticate)


class ModelBackend(InactiveMixin, DjangoModelBackend):
    pass


class RegistrationProfileBackend(ModelBackend):

    def authenticate(self, activation_key=None):
        return RegistrationProfile.objects.activate_user(activation_key) or None


class EmailBackend(InactiveMixin, DjangoModelBackend):

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


class AbModelBackend(DjangoModelBackend):
    # Added for backward compatibility
    pass
