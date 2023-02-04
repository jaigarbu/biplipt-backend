import graphene

from app.graphql.Type.user import UserSessionType


class LocalesType(graphene.ObjectType):
	'tipo de dato para la lista de idiomas del sistema'
	name = graphene.String()
	locale = graphene.String()


class SystemType(graphene.ObjectType):
	'tipo de dato del sistema'
	name = graphene.String()
	live = graphene.Boolean()
	message = graphene.String()
	register = graphene.Boolean()
	social = graphene.Boolean()
	facebook = graphene.Boolean()
	google = graphene.Boolean()
	apple = graphene.Boolean()
	version = graphene.String()


class AppType(graphene.ObjectType):
	'Tipo de dato de la aplicación'
	title = graphene.String()
	keywords = graphene.String()
	description = graphene.String()


class AppDataType(graphene.ObjectType):
	'tipo de dato para la consulta del sistema'
	app = graphene.Field(SystemType)
	page = graphene.Field(AppType)
	loggedIn = graphene.Boolean()
	user = graphene.Field(UserSessionType)
	locale = graphene.String()
	dir = graphene.String()
	locales = graphene.List(LocalesType)
  
