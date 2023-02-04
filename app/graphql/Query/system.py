import asyncio
from time import sleep
import graphene
from graphql import GraphQLError
from app.controllers.system import SystemController

from app.graphql.Type.system import AppDataType


class SystemType(graphene.ObjectType):
  
  _ = graphene.Field(AppDataType)
  
  # resolvers
  def resolve__(root, info):
    try:
      system = SystemController.get_system(info.context)
      return system
    except Exception as e:
      return GraphQLError(_('Internal Server Error. Please try again later'))



class SystemApp(graphene.ObjectType):
  app = graphene.Field(AppDataType)
  
  @classmethod
  async def subscribe_app(root, info):
    while True:
      yield SystemController.get_system(info.context)
      await asyncio.sleep(1)
