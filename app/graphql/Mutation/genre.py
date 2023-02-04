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
      addedBy = graphene.String(required=False)
   
   @classmethod
   def mutate(cls, root, info, **kwargs):
      try:
         genre = GenreController.createGenre(inputs=kwargs, headers=info.context)
         return CreateGenre(code=200, message=_("Género creado correctamente"), data=genre)
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except BaseException as e:
         print(e.args)
         return GraphQLError('Internal Server Error')