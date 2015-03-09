# -*- coding: utf-8 -*-

from mongoengine.connection import connect, ConnectionError


class ConnectionProxy(object):

    __mongo = None
    __connection_kwargs = {}

    def __init__(self, *args, **kwargs):
        self.__connection_args = args[:]
        self.__connection_kwargs = kwargs.copy()

    def __repr__(self):
        return repr(self.__mongo)

    def connect(self):
        try:
            self.__mongo = connect(*self.__connection_args, **self.__connection_kwargs).avtobazar
        except ConnectionError:
            pass
        return self.__mongo

    def check_mongo(self):
        if self.__mongo is None:
            self.connect()

    def __nonzero__(self):
        self.check_mongo()
        return not self.__mongo is None

    def __getattr__(self, name):
        self.check_mongo()
        return getattr(self.__mongo, name)
