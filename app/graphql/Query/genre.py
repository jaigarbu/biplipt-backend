import graphene
from graphql import GraphQLError

from app.controllers.genre import GenreController
from app.graphql.Enum.orderBy import OrderBy
from app.graphql.Type.genre import GenreType
from app.utils.exceptions import HttpError, ValidationError


class GenreQuery(graphene.ObjectType):
   
   getGenre = graphene.Field(GenreType, id=graphene.ID(required=False), name=graphene.String(required=False), dns=graphene.String(required=False))
   getGenres = graphene.List(GenreType, orderBy=graphene.Argument(OrderBy), offset=graphene.Int(), limit=graphene.Int())
   
   # resolvers
   def resolve_getGenre(root, info, id=None, name=None, dns=None):
      if (id != None):
         field = "id"
         value = id
      elif (name != None):
         field = 'name'
         value = name
      elif (dns != None):
         field = 'dns'
         value = dns
      else:
         field = 'id'
         value = 0
         
      try:
         genre = GenreController.getGenre(field=field, value=value, headers=info.context.META)
         return genre
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception as e:
         print(e.args)
         return GraphQLError('Internal Server Error')
   
   
   def resolve_getGenres(root, info, orderBy=None, offset=None, limit=None):
      try:
         genres = GenreController.getGenres(orderBy=orderBy, offset=offset, limit=limit, headers=info.context.META)
         return genres
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception as e:
         print(e.args)
         return GraphQLError('Internal Server Error')
   