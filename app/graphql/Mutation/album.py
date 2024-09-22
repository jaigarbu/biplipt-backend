import os
import shutil

import graphene
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext as _
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError

from app.controllers.album import AlbumController
from app.controllers.uploads import UploadsController
from app.graphql.Enum.cofiguration import AlbumTypeEnum, ItemVisibilityEnum
from app.graphql.Input.globals import FeaturingInput
from app.graphql.Type.album import AlbumType
from app.utils.exceptions import HttpError, ValidationError
from core.settings import BASE_DIR


class CreateAlbum(graphene.Mutation):
   code = graphene.Int(required=True)
   message = graphene.String(required=True)
   data = graphene.Field(AlbumType)
   
   class Arguments:
      visibility = graphene.Argument(ItemVisibilityEnum, required=True)
      tags = graphene.String(required=True)
      name = graphene.String(required=True)
      nativeName = graphene.String()
      type = graphene.Argument(AlbumTypeEnum, required=True)
      country = graphene.String(required=True)
      year = graphene.Int()
      number = graphene.Int()
      language = graphene.String(required=True)
      appleMusicID = graphene.String()
      deezerID = graphene.String()
      spotifyID = graphene.String()
      youTubeID = graphene.String()
      youTubeMusicID = graphene.String()
      cover = Upload()
      color = graphene.String()
      vibrantColor = graphene.String()
      artist = graphene.ID(required=True)
      genres = graphene.List(graphene.String, required=True)
      ft = graphene.List(FeaturingInput)
   
   def mutate(root, info, **kwargs):
      try:
         album = AlbumController.createAlbum(inputs=kwargs, headers=info.context.META)
         return CreateAlbum(code=200, message=_('Álbum creado correctamente'), data=album)
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception as e:
         print(e.args)
         return GraphQLError('Internal Server Error')