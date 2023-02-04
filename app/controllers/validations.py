import re

from django.utils.translation import gettext as _

from app.constants.regExp import (EXP_COUNTRY_CODE, EXP_EMAIL, EXP_GENDER,
                                  EXP_LANGUAGE, EXP_NAME, EXP_TOKEN_URL,
                                  EXP_USERNAME)
from app.utils.exceptions import ValidationError


class ValidationsController():  
   
   @classmethod
   def validateRegisterUser(cls, params: dict):
      """Valida los campos necesarios para el registro de un usuario
      
      :param `params: dict` — Campos para la creacion de una cuenta
      """    
      cls.val_name(params.get('name'))
      cls.val_name(params.get('lastName'), 'lastname')
      cls.val_country_code(params.get('country'))
      cls.val_gender(params.get('gender'))
      cls.val_language(params.get('language'))
      cls.val_username(params.get('username'))
      cls.val_email(params.get('email'))
      cls.val_match_password(params.get('password'), params.get('passwordVerify'))
   
   
   @classmethod
   def val_email(cls, email: str):
      'Valida un E-mail'
      if not re.search(EXP_EMAIL, email):
         raise ValidationError(_('Formato de correo electrónico inválido'), 'email')


   @classmethod
   def val_id(cls, id):
      'Valida un ID'
      if not isinstance(id, int) or id < 1:
         raise ValidationError(_('ID inválido'), 'id')


   @classmethod
   def val_username(cls, username: str):
      'Valida un nombre de usuario'
      if re.search(EXP_USERNAME, username) == False:
         raise ValidationError(_('El nombre de usuario ingresado no es válido'), 'username')


   @classmethod
   def val_name(cls, name: str, field: str = 'name'):
      'Valida un nombre. Usa la regExp `[a-z]+(\s[a-z]+)`'
      if not re.match(EXP_NAME, name, re.IGNORECASE):
         raise ValidationError(_('El nombre ingresado no es válido'), field)


   @classmethod
   def val_country_code(cls, code):
      'Valida un codigo de pais'
      if not re.search(EXP_COUNTRY_CODE, code):
         raise ValidationError(_('El pais ingresado no es válido'), 'country')


   @classmethod
   def val_gender(cls, gender):
      'Valida un género'
      if not re.search(EXP_GENDER, gender):
         raise ValidationError(_('El género ingresado no es válido'), 'gender')


   @classmethod
   def val_language(cls, language):
      'Valida un codigo de lenguaje'
      if not re.search(EXP_LANGUAGE, language):
         raise ValidationError(_('El idioma seleccionado no es válido'), 'language')

  
   @classmethod
   def val_match_password(cls, password: str, passwordVerify: str):
      'Comprueba match de contraseñas'
      if password != passwordVerify:
         raise ValidationError(_('Las contraseñas no cohiciden'), 'password')


   @classmethod
   def val_dns(cls, dns):
      'Valida un DNS'
      if not re.search(EXP_TOKEN_URL, dns):
         raise ValidationError(_('El DNS ingresado no es válido'), 'DNS')
   
   
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