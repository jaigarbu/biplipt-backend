import graphene
from django.utils.translation import gettext as _
from graphql import GraphQLError

from app.controllers.genre import GenreController
from app.graphql.Enum.cofiguration import ItemVisibilityEnum
from app.graphql.Type.genre import GenreType
from app.utils.exceptions import HttpError, ValidationError


class CreateGenre(graphene.Mutation):
   code = graphene.Int(required=True)
   message = graphene.String(required=True)
   data = graphene.Field(GenreType)
   
   class Arguments:
      visibility = graphene.Argument(ItemVisibilityEnum, required=True)
      name = graphene.String(required=True)
   
   def mutate(root, info, **kwargs):
      try:
         genre = GenreController.createGenre(inputs=kwargs, headers=info.context.META)
         return CreateGenre(code=200, message=_("Género creado correctamente"), data=genre)
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except BaseException as e:
         print(e.args)
         return GraphQLError('Internal Server Error')


class DeleteGenre(graphene.Mutation):
   code = graphene.Int(required=True)
   message = graphene.String(required=True)
   id = graphene.ID(required=True)
   
   class Arguments:
      id = graphene.ID(required=True)
   
   def mutate(root, info, id):
      try:
         GenreController.deleteGenre(id=id, headers=info.context.META)
         return DeleteGenre(code=200, message=_('Género eliminado correctamente'), id=id)
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except BaseException as e:
         print(e.args)
         return GraphQLError('Internal Server Error')