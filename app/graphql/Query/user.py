import graphene
from graphql import GraphQLError

from app.controllers.user import UserController
from app.graphql.Enum.orderBy import OrderBy
from app.graphql.Type.user import UserType
from app.utils.exceptions import HttpError, ValidationError


class UserQuery(graphene.ObjectType):
   
   getUser = graphene.Field(UserType, id=graphene.Int(required=False), username=graphene.String(required=False), email=graphene.String(required=False))
   getUsers = graphene.List(UserType, orderBy=graphene.Argument(OrderBy), offset=graphene.Int(), limit=graphene.Int())
   
   
   # resolvers
   def resolve_getUser(root, info, id=None, username=None, email=None):
      if (id != None):
         field = "id"
         value = id
      elif (username != None):
         field = 'username'
         value = username
      elif (email != None):
         field = 'email'
         value = email
      else:
         field = 'id'
         value = 0
      
      try:
         data = UserController.getUser(field=field, value=value, headers=info.context.META)
         return data
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception:
         return GraphQLError('Internal Server Error')
   
   
   def resolve_getUsers(root, info, orderBy=None, offset=None, limit=None):
      try:
         users = UserController.getUsers(orderBy=orderBy, offset=offset, limit=limit, headers=info.context.META)
         return users
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception as e:
         print(e.args)
         return GraphQLError('Internal Server Error')