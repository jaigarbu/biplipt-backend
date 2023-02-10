from hashlib import sha256

from django.db.models import Q
from django.utils.translation import gettext as _

from app.constants.config import JWS_KEY_ACTIVATION
from app.controllers.auth import AuthController
from app.controllers.token import TokenController
from app.controllers.validations import ValidationsController
from app.functions.chars import random_numbers
from app.functions.system import get_IP
from app.models.admins import Admin
from app.utils.exceptions import HttpError


class AdminController:
   
   adminAlreadyExist = _('El administrador ya existe')
   
   @classmethod
   def createAdmin(cls, inputs: dict, headers: dict) -> Admin:
      """Crea un administrador, moderador o artista en el sistema
      
      :param `inputs: dict` — Campos necesarios para la creación
      :param `headers: dict` — Headers http de la consulta actual
      :return — Admin
      """
      # comprabar permisos de creacion de administrador
      session = AuthController.validate_session(headers=headers)
      if not isinstance(session, dict) or session.get('group') != 1:
         raise HttpError(AuthController.unauthorized, 401)
      
      # validar los campos de administrador
      ValidationsController.validateRegisterAdmin(params=inputs)
      
      # verificar que no exista el administrador a registrar
      # admin = Admin.objects.filter(email=inputs.get('email')).exists()
      admin = Admin.objects.filter(Q(email=inputs.get('email'), cellphone=inputs.get('cellphone'), _connector=Q.OR)).exists()
      if admin:
         raise HttpError(cls.adminAlreadyExist, 400)
      
      # seguridad a la cuenta
      passwordHash = AuthController.secure_password(inputs.get('password'))
      
      # creación de codigos de activacion de cuenta
      activationPin = random_numbers(6)
      activationKey = TokenController.singToken(payload={'pin':sha256(activationPin.encode('utf-8')).hexdigest()}, key=JWS_KEY_ACTIVATION)
      
      print(inputs)
      # creacion de admnistrador
      data = Admin.objects.create(
         group=inputs.get('group').value,
         status=inputs.get('status').value,
         verify=False,
         signature=None,
         name=inputs.get('name'),
         lastName=inputs.get('lastName'),
         country=inputs.get('country'),
         cellphone=inputs.get('cellphone'),
         gender=inputs.get('gender'),
         birthdate=inputs.get('birthdate'),
         email=inputs.get('email'),
         password=passwordHash,
         masterKey=None,
         lastSeen=None,
         ip=get_IP(headers),
         activationKey=activationKey
      )
      
      # enviar correo electronico con codigo de confirmacion
      print(f"Codigo activación admin: {activationPin}")
      
      return data
      
      
      