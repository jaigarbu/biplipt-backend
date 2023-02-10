import graphene
from django.utils.translation import gettext as _
from graphql import GraphQLError

from app.controllers.admin import AdminController
from app.graphql.Enum.cofiguration import AdminStatusEnum, UserStatusEnum
from app.graphql.Type.admin import AdminType
from app.utils.exceptions import HttpError, ValidationError


class CreateAdmin(graphene.Mutation):
   code = graphene.Int(required=True)
   message = graphene.String(required=True)
   data = graphene.Field(AdminType, required=True)
   
   class Arguments:
      group = graphene.Argument(AdminStatusEnum, required=True)
      status = graphene.Argument(UserStatusEnum, required=True)
      name = graphene.String(required=True)
      lastName = graphene.String(required=True)
      country = graphene.String(required=True)
      cellphone = graphene.String(required=True)
      gender = graphene.String(required=True)
      birthdate = graphene.Date(required=True)
      email = graphene.String(required=True)
      password = graphene.String(required=True)
      passwordVerify = graphene.String(required=True)
   
   def mutate(root, info, **kwargs):
      try:
         admin = AdminController.createAdmin(inputs=kwargs, headers=info.context.META)
         return CreateAdmin(code=200, message=_("Adminitrador agregado correctamente"), data=admin)
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception as e:
         print(e.args)
         return GraphQLError('Internal Server Error')