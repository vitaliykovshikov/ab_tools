#encoding: utf-8

from mongoengine import fields
from mongoengine.document import Document


class UserData(Document):

    user = fields.IntField(primary_key=True)
    sessions = fields.ListField(fields.StringField())


class InactiveUser(Document):

    user = fields.IntField(primary_key=True)
    password = fields.StringField()
    date_registered = fields.DateTimeField()
    sms_text = fields.StringField()
    sms_sended = fields.BooleanField(default=False)
    advert_activated = fields.BooleanField(default=False)
