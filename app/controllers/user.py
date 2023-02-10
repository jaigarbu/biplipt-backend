from hashlib import sha256

from django.db.models import Q
from django.utils.translation import gettext as _

from app.constants.config import JWS_KEY_ACTIVATION
from app.controllers.auth import AuthController
from app.controllers.token import TokenController
from app.controllers.validations import ValidationsController
from app.functions.chars import random_numbers
from app.functions.system import get_IP
from app.models.users import User
from app.utils.exceptions import HttpError


class UserController():

   offset = 0
   limit = 10
   userNotExist = _('El usuario no existe')
   userBlock = _('Esta cuenta se encuentra bloqueada')
   
   @classmethod
   def getUser(cls, field: str, value: any, headers: dict) -> User:
      """Consulta un usuario de la base de datos
      
      :param `field: str` — Campo por el que se buscará el usuario
      :param `value: any` — Valor por el que se buscará el usuario
      :param `headers: dict` — Encabezados GraphQL de la consulta actual
      :return — User
      """
      # determinar session actual
      session = AuthController.validate_session(headers=headers)
      
      try:
         # Determinar el tipo del campo de busqueda y realizar la consulta
         if field == 'id':
            ValidationsController.val_id(value)
            user = User.objects.get(id=value)
         elif field == 'email':
            ValidationsController.val_email(value)
            user = User.objects.get(email=value)
         elif field == "username":
            ValidationsController.val_username(value)
            user = User.objects.get(username=value)
         else:
            raise HttpError(cls.userNotExist, 404)
         
         # determinar visibilidad y estado de cuenta antes de retornar
         # se validan permisos de usuario para ver la cuenta
         userFilter = ['suspended', 'restricted', 'unverified']
         if user.status in userFilter and not AuthController.val_allow(payload=session, group=5):
            raise HttpError(cls.userNotExist, 404)
         if user.status == "block" and not AuthController.val_allow(payload=session, group=1):
            raise HttpError(cls.userBlock, 401)
            
         return user
      except User.DoesNotExist:
         raise HttpError(cls.userNotExist, 404)
         
   
   @classmethod
   def getUsers(cls, headers: dict, orderBy: any = None, offset: int|None = None, limit: int|None = None):
      """Consulta varios usuarios de la base de datos
      
      :param `headers: dict` — Headers Http de la consulta actual
      :param `orderBy: str | None` — Orden en que se mostraán los usuarios. Default `None`
      :param `offset: int | None` — Inicio de la consulta. Default `None`
      :param `limit: int | None` — Cantindad de usuarios a consultar. Default `None`
      :return — list
      """
      # Obteber orderBy offset y limit en caso de existir
      if orderBy != None:
         line = orderBy.value.partition('_')
         order = line[0] if line[2] == "asc" else f'-{line[0]}'
      else:
         order = 'id'
      minimun = offset if offset != None else cls.offset
      maximun = limit if limit != None else cls.limit
      
      # Determinar session actual
      session = AuthController.validate_session(headers=headers)
      
      if isinstance(session, dict): 
         # Realizar la consulta de acuerdo a los permisos de usuario para visibilizar
         if AuthController.val_allow(session, 1):
            data = User.objects.all().order_by(order)[minimun:maximun]
            return data
         
         if AuthController.val_allow(session, 5):
            data = User.objects.all().exclude(status="block").order_by(order)[minimun:maximun]
            return data
         
      # busqueda por defecto
      data = User.objects.filter(status="active").all().order_by(order)[minimun:maximun]
      return data    
      
   
   @classmethod
   def createUser(cls, inputs: dict, headers: dict) -> User:
      """Crea una un usuario en la base de datos
      
      :param `inputs: dict` — Datos necesarios para crear un usuario
      :param `headers: any` — Headers Http de la consulta actual
      :return — User
      """    
      # validar los campos del usuario
      ValidationsController.validateRegisterUser(inputs)
      
      # validar disponibilidad y creacion de usuario
      user = User.objects.filter(Q(email=inputs.get('email'), username=inputs.get('username'), _connector=Q.OR)).exists()
      if user:
         raise HttpError(_('No podemos registrar su cuenta porque estas credenciales ya existen'), 400)
      
      # seguridad a la contraseña
      passwordHash = AuthController.secure_password(password=inputs.get('password'))
      
      # creación de codigos de activacion de cuenta
      activationPin = random_numbers(6)
      activationKey = TokenController.singToken(payload={'pin':sha256(activationPin.encode('utf-8')).hexdigest()}, key=JWS_KEY_ACTIVATION)
      
      # creacion de susuario en base de datos
      newUser = User.objects.create(
         status=inputs.get('status').value,
         name=inputs.get('name'),
         lastName=inputs.get('lastName'),
         birthdate=inputs.get('birthdate'),
         country=inputs.get('country'),
         gender=inputs.get('gender'),
         language=inputs.get('language'),
         username=inputs.get('username'),
         email=inputs.get('email'),
         password=passwordHash,
         activationKey=activationKey,
         ip=get_IP(headers),
         photo=None
      )
      
      # Envio de correo electronico de activación de cuenta
      print(activationPin)
      return newUser
    
      
   @classmethod
   def deleteUser(cls, id: any, headers: dict) -> bool:
      """Elimina una cuenta de usuario
      
      :param `id: int` — ID del usuario a eliminar
      :param `headers: any` — Headers Http de la consulta actula
      :return — bool
      """
      # Comprobar la session actual
      payload = AuthController.validate_session(headers=headers)
      if not payload:
         raise HttpError(AuthController.unauthorized, 401)
      
      try:
         # Comprobar existencia de cuenta y permisos de usuario
         user = User.objects.get(id=id)
         if payload.get('group') != 1 and (user.status == 'block' or user.id != payload.get('id')):
            raise HttpError(AuthController.unauthorized, 401)
         
         # Eliminar usuario
         user.delete()
         return True
      except User.DoesNotExist as e:
         raise HttpError(_('La cuenta seleccionada no existe'), 404)
