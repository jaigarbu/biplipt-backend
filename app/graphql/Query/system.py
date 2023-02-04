import graphene
from django.utils.translation import gettext as _
from graphql import GraphQLError

from app.controllers.system import SystemController
from app.graphql.Type.system import AppDataType


class SystemQuery(graphene.ObjectType):
   
   _ = graphene.Field(AppDataType)
   
   # resolvers
   def resolve__(root, info):
      try:
         system = SystemController.get_system(info.context)
         return system
      except Exception as e:
         return GraphQLError(_('Internal Server Error. Please try again later'))
      
