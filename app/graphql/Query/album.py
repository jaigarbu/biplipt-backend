import graphene
from django.utils.translation import gettext as _
from graphql import GraphQLError

from app.controllers.album import AlbumController
from app.graphql.Enum.orderBy import OrderBy
from app.graphql.Type.album import AlbumType
from app.utils.exceptions import HttpError, ValidationError


class AlbumQuery(graphene.ObjectType):
   
   getAlbum = graphene.Field(AlbumType, id=graphene.ID(required=False), dns=graphene.String(required=False), name=graphene.String(required=False))
   getAlbums = graphene.List(AlbumType, orderBy=graphene.Argument(OrderBy), offset=graphene.Int(), limit=graphene.Int())
   
   # Resolvers
   def resolve_getAlbum(root, info, id=None, dns=None, name=None):
      # Determinar campo de busqueda
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
         return GraphQLError(_('Error de Consulta, asegurate de enviar almenos un campo para el filtro'))
         
      try:
         album = AlbumController.getAlbum(field=field, value=value, headers=info.context.META)
         return album
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception as e:
         print(e.args)
         return GraphQLError('Internal Server Error')
   
   
   def resolve_getAlbums(root, info, orderBy=None, offset=None, limit=None):
      try:
         albums = AlbumController.getAlbums(orderBy=orderBy, offset=offset, limit=limit, headers=info.context.META)
         return albums
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception as e:
         print(e.args)
         return GraphQLError('Internal Server Error')