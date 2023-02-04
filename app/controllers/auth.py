
from django.utils.translation import gettext as _

from app.constants.config import JWS_KEY
from app.controllers.token import TokenController
from app.controllers.user import UserController
from app.controllers.validations import ValidationsController
from app.models.users import Users
from app.utils.exceptions import HttpError, ValidationError


class AuthController:
   
   sessionInvalid = _('Tu sessión ha expirado. Por favor ingresa de nuevo para continuar')
   unauthorized = _('Usted no está autorizado')
   
   @classmethod
   def login(cls, email: str, password: str) -> str:
      """Inicia sesión en el sistema
      
      :param `email: str` — Correo electrónico
      :param `password: str` — Contraseña
      :return — str
      """
      # validar datos de sesion
      ValidationsController.val_email(email=email)
      
      try:
         # validar exiatencia de cuenta y credenciales
         user = Users.objects.get(email=email)
         checkPw = UserController.verify_password(password=password, passwordHash=user.password)
         if not checkPw:
            raise ValidationError(_('Credenciales de acceso inválidas. Por favor, verifiquelas'), 'credential')
         
         # creacion de payload de token de session
         payload = {
            'id': user.ID,
            'group': 1,
            'name': user.name,
            'lastName': user.lastName,
         }
         
         token = TokenController.singToken(payload=payload, key=JWS_KEY, expiration=604800)
         return token
      except Users.DoesNotExist as e:
         raise HttpError(_('Esta cuenta no existe'), 400)
   
   
   @classmethod
   def validate_session(cls, token: str|None, key: str|None=None) -> dict|bool:
      """Valida un asession de usuario mediante un JWT
      
      :param `token: str | None` — Token de session
      :param `key: str` — JWK usada para firmar el token
      :return — dict|bool
      """
      clave = key if key else JWS_KEY
      payload = TokenController.verifyJWSToken(key=clave, token=token)
      return payload    
   