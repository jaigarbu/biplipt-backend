import graphene
from graphene_django import DjangoObjectType

from app.models.users import Users


class UserType(DjangoObjectType):
   class Meta:
      model = Users
      exclude = ('password', 'activationKey')


class UserSessionType(graphene.ObjectType):
	id = graphene.ID()
	ame = graphene.String()
	roup = graphene.Int()
	hoto = graphene.String()
	sid = graphene.String()
	dmin = graphene.Boolean()
	dminHash = graphene.String()