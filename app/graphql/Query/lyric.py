import graphene
from django.utils.translation import gettext as _
from graphql import GraphQLError

from app.controllers.lyric import LyricController
from app.graphql.Enum.orderBy import OrderBy
from app.graphql.Type.lyric import LyricType
from app.utils.exceptions import HttpError, ValidationError


class LyricQuery(graphene.ObjectType):
   
   getLyric = graphene.Field(LyricType, id=graphene.ID(required=False), dns=graphene.String(required=False))
   getLyrics = graphene.List(LyricType, orderBy=graphene.Argument(OrderBy), offset=graphene.Int(required=False), limit=graphene.Int(required=False))
   
   # resolvers
   def resolve_getLyric(root, info, id=None, dns=None):
      # determiar campo de bsuqueda de la letra
      if id:
         field = 'id'
         value = id
      elif dns:
         field = 'dns'
         value = dns
      else:
         return GraphQLError(_('Error de consulta. Especifica un filtro para buscar'))
      
      try:
         data = LyricController.getLyric(field=field, value=value, headers=info.context.META)
         return data
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception:
         return GraphQLError('Internal Server Error')
   
   def resolve_getLyrics(root, info, orderBy=None, offset=None, limit=None):
      try:
         data = LyricController.getLyrics(headers=info.context.META, orderBy=orderBy, offset=offset, limit=limit)
         return data
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception:
         return GraphQLError('Internal Server Error')