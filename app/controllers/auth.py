from codecs import decode, encode
from typing import Any, NewType

import bcrypt
from django.utils.translation import gettext as _

from app.constants.config import JWS_KEY
from app.controllers.token import TokenController
from app.controllers.validations import ValidationsController
from app.models.users import User
from app.utils.exceptions import HttpError, ValidationError


class AuthController:
   """Controlador de procesos relacionados con la autenticacion y seguridad de las cuentas y adminstraciones
   internas del sistema
   
   :raises `ValidationError` — Excepcion para errores de validacion
   :raises `HttpError` — Excpecion para errores de peticiones HTTP
   """
   
   cost = 14
   sessionInvalid = _('Tu sessión ha expirado. Por favor ingresa de nuevo para continuar')
   unauthorized = _('Usted no está autorizado para realizar esta operación')
   notAvailable = _('Lo sentimos el recurso solicitado no está disponible')
   restricted = _('Lo sentimos el recurso solicitado se encuentra restringido')
   
   @classmethod
   def login(cls, email: str, password: str, headers: dict[str, Any]) -> str:
      """Inicia sesión en el sistema
      
      :param `email: str` — Correo electrónico
      :param `password: str` — Contraseña
      :return — str
      """
      invalidCredentials = _('Credenciales de acceso inválidas. Por favor, verifíquelas e intente nuevamente')
      
      # validar datos de sesion
      ValidationsController.val_email(email=email)
      
      # comprobar que no hay una session valida activa
      session = cls.validate_session(headers=headers)
      if isinstance(session, dict):
         return headers['HTTP_AUTHORIZATION']
      
      try:
         # validar exiatencia de cuenta y credenciales
         user = User.objects.get(email=email)
         checkPw = cls.verify_password(password=password, passwordHash=user.password)
         if not checkPw:
            raise ValidationError(invalidCredentials, 'credential')
         
         # creacion de payload de token de session
         payload = {
            'id': user.id,
            'group': 1,
            'name': user.name,
            'lastName': user.lastName,
         }
         
         token = TokenController.singToken(payload=payload, key=JWS_KEY, expiration=604800)
         return token
      except User.DoesNotExist:
         raise HttpError(invalidCredentials, 400)
   
   
   @classmethod
   def validate_session(cls, headers: dict[str, Any], key: str|None = None) -> dict[str, str|int]|bool:
      """Verifica si existe una session actual válida
      
      :param `headers: dict` — Headers http de la consulta actual
      :param `key: str | None` — JWK usada para comprobar la firma del token. Default `None`
      :return — dict|bool
      """
      token = headers.get('HTTP_AUTHORIZATION', None)
      clave = key if key else JWS_KEY
      payload = TokenController.verifyJWSToken(key=clave, token=token)
      return payload


   @classmethod
   def val_allow(cls, payload: dict[str, str|int]|bool, group: int) -> bool:
      """Comprueba los permisos de un usuario
      
      :param `payload: dict | bool` — Carga util de un JWT de session
      :param `group: int` — Grupo al que pertenece el usuario
      :return — bool
      
      Los grupos para la validación son:
      * `1` Solo adminitrador
      * `2` Solo moderador
      * `3` Solo artista
      * `4` Todos los usuarios logeados del sistema
      * `5` Todos los moderadores (administrador, moderador, artista)
      * `6` Solo administrador y artista
      """
      allow = payload.get('group', False) if isinstance(payload, dict) else False
      if (not allow and group < 5) or (group < 5 and allow != group):
         return False
      if (not allow and group == 5) or (group == 5 and allow > 3):
         return False
      if (not allow and group == 6) or (group == 6 and allow > 2):
         return False
      return True
   
   
   @classmethod
   def secure_password(cls, password: str) -> str:
      """Encrypta una contraseña
      
      :param `password: str` — Contraseña a cifrar
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
   
   
   @classmethod
   def validate_permissions(cls, session: dict|bool, visibility: str):
      """Valida los permisos del usuario actual para consultar un recurso
      
      :param `session: dict | bool` — Payload de session actual del usuario
      :param `visibility: str` — Visibilidad actual del recurso
      :param `messages: dict` — Diccionario con los mensajes de error para cada caso de valicación
      :raises `HttpError` — Excepcion patra errores HTTP
      
      Las claves del diccionario para los mensajes de error son los siguintes:
      * `404` Mensaje de error para recursos bloqueados o privados
      * `401` Mensaje de error para recursos restringidos
      """      
      if visibility == 'block' and not AuthController.val_allow(session, 1):
         raise HttpError(cls.notAvailable, 404)
            
      if visibility == 'private' and not AuthController.val_allow(session, 6):
         raise HttpError(cls.notAvailable, 404)
            
      if visibility == 'restricted' and not AuthController.val_allow(session, 5):
         raise HttpError(cls.restricted, 401)