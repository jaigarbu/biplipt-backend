from graphene_django import DjangoObjectType

from app.models.admins import Admin


class AdminType(DjangoObjectType):
   class Meta:
      model = Admin
      exclude = ('password', 'signature', 'masterKey', 'activationKey')