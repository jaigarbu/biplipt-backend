import re

from django.utils.translation import gettext as _

from app.constants.regExp import (EXP_CELLPHONE, EXP_COUNTRY_CODE, EXP_EMAIL,
                                  EXP_GENDER, EXP_LANGUAGE, EXP_NAME,
                                  EXP_TOKEN_URL, EXP_USERNAME)
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
   def validateRegisterAdmin(cls, params: dict):
      """Valida los campos necesarios para el registro de un administrador, moderador o artista
      
      :param `params: dict` — Campos para la creacion de una cuenta de adminitracion o modearción
      """
      cls.val_name(params.get('name'))
      cls.val_name(params.get('lastName'), 'lastname')
      cls.val_country_code(params.get('country'))
      cls.val_cellphone(params.get('cellphone'))
      cls.val_gender(params.get('gender'))
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
      if int(id) < 1:
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
   def val_cellphone(cls, cellphone):
      'valida un numero de telefono con formato internacional'
      if not re.search(EXP_CELLPHONE, cellphone):
         raise ValidationError(_('El número de teléfono no es válido'))
   
   
   @classmethod
   def set_queryOrderBy(cls, orderBy: str|None) -> str:
      """Valida y establece el orderBy de una sonsulta dentro de un controlador
      
      :param `orderBy: str | None` — Orden de la consulta en formato `campo_order`
      :return — dict
      """
      if orderBy != None:
         line = orderBy.value.partition('_')
         order = line[0] if line[2] == "asc" else f'-{line[0]}'
      else:
         order = 'id'
      return order