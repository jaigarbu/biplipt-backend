import graphene
from django.utils.translation import gettext as _
from graphql import GraphQLError

from app.controllers.auth import AuthController
from app.controllers.user import UserController
from app.graphql.Enum.cofiguration import UserStatusEnum
from app.graphql.Type.user import UserType
from app.utils.exceptions import HttpError, ValidationError


class CreateUser(graphene.Mutation):
   code = graphene.Int(required=True)
   message = graphene.String(required=True)
   data = graphene.Field(UserType)
   
   class Arguments:
      status = graphene.Argument(UserStatusEnum, required=True)
      name = graphene.String(required=True)
      lastName = graphene.String(required=True)
      birthdate = graphene.Date(required=True)
      country = graphene.String(required=True)
      gender = graphene.String(required=True)
      language = graphene.String(required=True)
      username = graphene.String(required=True)
      email = graphene.String(required=True)
      password = graphene.String(required=True)
      passwordVerify = graphene.String(required=True)
      
   @classmethod
   def mutate(cls, root, info, **kwargs):
      try:
         user = UserController.createUser(inputs=kwargs, headers=info.context)
         return CreateUser(code=200, message=_("Usuario creado correctamente"), data=user)
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception:
         return GraphQLError('Internal Server Error')


class DeleteUser(graphene.Mutation):
   code = graphene.Int(required=True)
   message = graphene.String(required=True)
   id = graphene.ID()
   
   class Arguments:
      id = graphene.ID(required=True)
   
   @classmethod
   def mutate(self, root, info, id):
      try:
         UserController.deleteUser(id=id, headers=info.context)
         msg = _('Cuenta eliminada correctamente')
         return DeleteUser(code=200, message=msg, id=id)
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception:
         return GraphQLError('Internal Server Error')


class LoginUser(graphene.Mutation):
   code = graphene.Int(required=True)
   message = graphene.String(required=True)
   token = graphene.String()
   
   class Arguments:
      email = graphene.String(required=True)
      password = graphene.String(required=True)
   
   @classmethod
   def mutate(self, root, info, email, password):
      try:
         token = AuthController.login(email=email, password=password)
         return LoginUser(code=200, message=_('Login Successfully'), token=token)
      except ValidationError as e:
         return GraphQLError(message=e.message)
      except HttpError as e:
         return GraphQLError(message=e.message)
      except Exception:
         return GraphQLError('Internal Server Error')