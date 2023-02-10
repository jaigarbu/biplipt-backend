from codecs import decode, encode
from tokenize import group

import bcrypt
from django.utils.translation import gettext as _

from app.constants.config import JWS_KEY
from app.controllers.token import TokenController
from app.controllers.validations import ValidationsController
from app.models.users import User
from app.utils.exceptions import HttpError, ValidationError


class AuthController:
   
   cost = 14
   sessionInvalid = _('Tu sessión ha expirado. Por favor ingresa de nuevo para continuar')
   unauthorized = _('Usted no está autorizado para realizar esta operación')
   
   @classmethod
   def login(cls, email: str, password: str, headers: dict) -> str:
      """Inicia sesión en el sistema
      
      :param `email: str` — Correo electrónico
      :param `password: str` — Contraseña
      :return — str
      """
      # validar datos de sesion
      ValidationsController.val_email(email=email)
      
      # comprobar que no hay una session valida activa
      session = cls.validate_session(headers=headers)
      if isinstance(session, dict):
         return headers.get('HTTP_AUTHORIZATION')
      
      try:
         # validar exiatencia de cuenta y credenciales
         user = User.objects.get(email=email)
         checkPw = cls.verify_password(password=password, passwordHash=user.password)
         if not checkPw:
            raise ValidationError(_('Credenciales de acceso inválidas. Por favor, verifiquelas'), 'credential')
         
         # creacion de payload de token de session
         payload = {
            'id': user.id,
            'group': 1,
            'name': user.name,
            'lastName': user.lastName,
         }
         
         token = TokenController.singToken(payload=payload, key=JWS_KEY, expiration=604800)
         return token
      except User.DoesNotExist as e:
         raise HttpError(_('Esta cuenta no existe'), 401)
   
   
   @classmethod
   def validate_session(cls, headers: dict, key: str|None = None) -> dict|bool:
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
   def val_allow(cls, payload: dict|bool, group: int) -> bool:
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