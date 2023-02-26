import graphene
from django.utils.translation import gettext as _
from graphql import GraphQLError

from app.controllers.artist import ArtistController
from app.graphql.Enum.orderBy import OrderBy
from app.graphql.Type.artist import ArtistType
from app.utils.exceptions import HttpError, ValidationError


class ArtistQuery(graphene.ObjectType):
   
   getArtist = graphene.Field(ArtistType, id=graphene.ID(required=False), dns=graphene.String(required=False), name=graphene.String(required=False))
   getArtists = graphene.List(ArtistType, orderBy=graphene.Argument(OrderBy), offset=graphene.Int(), limit=graphene.Int())
   
   # Resolvers
   def resolve_getArtist(root, info, id=None, dns=None, name=None):
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
         artist = ArtistController.getArtist(field=field, value=value, headers=info.context.META)
         return artist
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception as e:
         print(e.args)
         return GraphQLError('Internal Server Error')
   
   def resolve_getArtists(root, info, orderBy=None, offset=None, limit=None):
      try:
         artists = ArtistController.getArtists(orderBy=orderBy, offset=offset, limit=limit, headers=info.context.META)
         return artists
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception as e:
         print(e.args)
         return GraphQLError('Internal Server Error')