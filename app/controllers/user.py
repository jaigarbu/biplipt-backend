from codecs import decode, encode
from datetime import datetime
from hashlib import sha256

import bcrypt
from django.db.models import Q
from django.utils.translation import gettext as _

from app.constants.config import JWS_KEY, JWS_KEY_ACTIVATION
from app.controllers.token import TokenController
from app.controllers.validations import ValidationsController
from app.functions.chars import random_numbers
from app.functions.system import get_IP
from app.models.users import Users
from app.utils.exceptions import HttpError


class UserController():

   cost = 14
   offset = 0
   limit = 10
   
   @classmethod
   def getUser(cls, field: str, value: any, headers) -> Users:
      """Consulta un usuario de la base de datos
      
      :param `field: str` — Campo por el que se buscará el usuario
      :param `value: any` — Valor por el que se buscará el usuario
      :param `headers: any` — Encabezados GraphQL de la consulta actual
      :return — User
      """    
      # Determinar el tipo del campo de busqueda y realizar la busqueda
      try:
         if field == 'ID':
            ValidationsController.val_id(value)
            user = Users.objects.get(id=value)
            return user
         elif field == 'email':
            ValidationsController.val_email(value)
            user = Users.objects.get(email=value)
            return user
         elif field == "usermane":
            ValidationsController.val_username(value)
            user = Users.objects.get(username=value)
            return user
         else:
            raise HttpError(_('El usuario no existe'), 400)
      except Users.DoesNotExist as e:
         raise HttpError(_('El usuario no existe'), 400)
         
   
   @classmethod
   def getUsers(cls, headers: any, orderBy: str|None = None, offset: int|None = None, limit: int|None = None):
      """Consulta varios usuarios de la base de datos
      
      :param `headers: any` — Headers Http de la consulta actual
      :param `orderBy: str | None` — Orden en que se mostraán los usuarios. Default `None`
      :param `offset: int | None` — Inicio de la consulta. Default `None`
      :param `limit: int | None` — Cantindad de usuarios a consultar. Default `None`
      :return — list
      """
      # Obteber orderBy offset y limit en caso de existir
      if orderBy != None:
         line = orderBy.value.partition('_')
         order = line[0] if line[2] == "ASC" else f'-{line[0]}'
      else:
         order = 'id'
      minimun = offset if offset != None else cls.offset
      maximun = limit if limit != None else cls.limit
         
      # Realizar la consulta
      data = Users.objects.all().order_by(order)[minimun:maximun]
      return data
   
   
   @classmethod
   def createUser(cls, inputs: dict, headers: any) -> Users:
      """Crea una un uruario en la base de datos
      
      :param `inputs: dict` — Datos necesarios para crear un usuario
      :param `headers: any` — Headers Http de la consulta actual
      :return — User
      """    
      # validar los campos del usuario
      ValidationsController.validateRegisterUser(inputs)
      
      # validar disponibilidad y creacion de usuario
      user = Users.objects.filter(Q(email=inputs.get('email'), username=inputs.get('username'), _connector=Q.OR)).exists()
      if user:
         raise HttpError(_('No podemos registrar su cuenta porque estas credenciales ya existen'), 400)
      
      # seguridad a la contraseña
      passwordHash = cls.__secure_password(password=inputs.get('password'))
      
      # creación de codigos de activacion de cuenta
      activationPin = random_numbers(6)
      activationKey = TokenController.singToken(payload={'pin':sha256(activationPin.encode('utf-8')).hexdigest()}, key=JWS_KEY_ACTIVATION)
      
      # creacion de susuario en base de datos
      newUser = Users.objects.create(
         status=inputs.get('status').value[0],
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
         registeredAt=datetime.now(),
         ip=get_IP(headers),
         photo=None
      )
      
      # Envio de correo electronico de activación de cuenta
      print(activationPin)
      return newUser
    
      
   @classmethod
   def deleteUser(cls, id: any, headers: any) -> bool:
      """Elimina una cuenta de usuario
      
      :param `id: int` — ID del usuario a eliminar
      :param `headers: any` — Headers Http de la consulta actula
      :return — bool
      """
      # Comprobar la session actual
      token = headers.META.get('HTTP_AUTHORIZATION', None)
      payload = TokenController.verifyJWSToken(key=JWS_KEY, token=token)
      if not payload:
         raise HttpError(_('Usted no está autorizado para realizar esta acción'), 401)
      
      try:
         # Comprobar permisos de usuario
         user = Users.objects.get(ID=id)
         if user.status == 'block' or user.ID != payload.get('id'):
            raise HttpError(_('Usted no está autorizado para realizar esta acción'), 401)
         
         # Eliminar usuario
         user.delete()
         return True
      except Users.DoesNotExist as e:
         raise HttpError(_('La cuenta seleccionada no existe'), 400)
      
   
   @classmethod
   def __secure_password(cls, password: str) -> str:
      """Encrypta una contraseña
      
      :param `password: str` — Contraseñ a cifrar
      :return — str
      """
      rawbites = encode(password)
      salt = bcrypt.gensalt(rounds=cls.cost)
      passwordHash = bcrypt.hashpw(password=rawbites, salt=salt)
      return decode(passwordHash)
   
   
   @classmethod
   def verify_password(cls, password: str, passwordHash: str) -> bool:
      """Verifica un hash de contraseña
      
      :param `password: str` — String con la contraseña del usuario
      :param `passwordHash: str` — String con el hash de la contraseña de la base de datos
      :return — bool
      """    
      bitesPass = password.encode()
      bitesHash = passwordHash.encode()
      verify = bcrypt.checkpw(password=bitesPass, hashed_password=bitesHash)
      return verify