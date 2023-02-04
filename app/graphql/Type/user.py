import graphene
from graphene_django import DjangoObjectType

from app.models.users import Users


class UserType(DjangoObjectType):
   class Meta:
      model = Users
      exclude = ('password', 'activationKey')


class UserSessionType(graphene.ObjectType):
	id = graphene.ID()
	name = graphene.String()
	group = graphene.Int()
	photo = graphene.String()
	ssid = graphene.String()
	admin = graphene.Boolean()
	adminHash = graphene.String()