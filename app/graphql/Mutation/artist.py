import graphene
from django.utils.translation import gettext as _
from graphql import GraphQLError

from app.controllers.artist import ArtistController
from app.graphql.Enum.cofiguration import ArtistTypeEnum, ItemVisibilityEnum
from app.graphql.Type.artist import ArtistType
from app.utils.exceptions import HttpError, ValidationError


class CreateArtist(graphene.Mutation):
   code = graphene.Int(required=True)
   message = graphene.String(required=True)
   data = graphene.Field(ArtistType)
   
   class Arguments:
      visibility = graphene.Argument(ItemVisibilityEnum, required=True)
      verify = graphene.Boolean(required=False)
      tags = graphene.String(required=True)
      name = graphene.String(required=True)
      nativeName = graphene.String()
      type = graphene.Argument(ArtistTypeEnum, required=True)
      country = graphene.String(required=True)
      year = graphene.String()
      appleMusicID = graphene.String()
      deezerID = graphene.String()
      spotifyID = graphene.String()
      youTubeID = graphene.String()
      youTubeMusicID = graphene.String()
      facebookID = graphene.String()
      instagramID = graphene.String()
      twitterID = graphene.String()
      web = graphene.String()
      # photo = graphene.Upload()
      # cover = graphene.Upload()
      color = graphene.String()
      vibrantColor = graphene.String()
      info = graphene.String()
      genre = graphene.ID(required=True)
   
   def mutate(root, info, **kwargs):
      try:
         artist = ArtistController.createArtist(inputs=kwargs, headers=info.context.META)
         return CreateArtist(code=200, message=_('Artista creado correctamente'), data=artist)
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception as e:
         print(e.args)
         return GraphQLError('Internal Server Error')


class UpdateArtist(graphene.Mutation):
   code = graphene.Int(required=True)
   message = graphene.String(required=True)
   data = graphene.Field(ArtistType)
   
   class Arguments:
      dns = graphene.String(required=True)
      visibility = graphene.Argument(ItemVisibilityEnum)
      verify = graphene.Boolean()
      tags = graphene.String()
      name = graphene.String()
      nativeName = graphene.String()
      type = graphene.Argument(ArtistTypeEnum)
      country = graphene.String()
      year = graphene.String()
      appleMusicID = graphene.String()
      deezerID = graphene.String()
      spotifyID = graphene.String()
      youTubeID = graphene.String()
      youTubeMusicID = graphene.String()
      facebookID = graphene.String()
      instagramID = graphene.String()
      twitterID = graphene.String()
      web = graphene.String()
      # photo = graphene.Upload()
      # cover = graphene.Upload()
      color = graphene.String()
      vibrantColor = graphene.String()
      info = graphene.String()
      # genre = graphene.ID()
   
   def mutate(root, info, **kwargs):
      try:
         artist = ArtistController.updateArtist(dns=kwargs['dns'], inputs=kwargs, headers=info.context.META)
         return CreateArtist(code=200, message=_('Artista modificado correctamente'), data=artist)
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception as e:
         print(e.args)
         return GraphQLError('Internal Server Error')
