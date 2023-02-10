import graphene
from graphene_django import DjangoObjectType

from app.models.users import User


class UserType(DjangoObjectType):
   class Meta:
      model = User
      exclude = ('password', 'activationKey')


class UserSessionType(graphene.ObjectType):
	id = graphene.ID()
	name = graphene.String()
	group = graphene.Int()
	photo = graphene.String()
	ssid = graphene.String()
	admin = graphene.Boolean()
	adminHash = graphene.String()