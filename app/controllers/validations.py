import re

from django.utils.translation import gettext as _

from app.constants.regExp import (EXP_CELLPHONE, EXP_COLOR_HEX,
                                  EXP_COUNTRY_CODE, EXP_EMAIL,
                                  EXP_FACEBOOK_PROFILE, EXP_GENDER,
                                  EXP_LANGUAGE, EXP_NAME, EXP_TAGS,
                                  EXP_TOKEN_URL, EXP_URL, EXP_URL_COMPLETE,
                                  EXP_URL_HASH, EXP_USERNAME)
from app.utils.exceptions import ValidationError


class ValidationsController():
   """Controlador de validaciones de campos y entradas de usuario"""
   
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
   def validateRegisterArtist(cls, params: dict):
      """Valida los campos necesario para crear un artista en la base de datos
      
      :param `params: dict` — Campos a validar
      """
      # Validar campos obligatorios
      cls.val_tags(params.get('tags'))
      cls.val_name(params.get('name'))
      cls.val_country_code(params.get('country'))
      
      # validar campos opcionales
      if 'year' in params:
         cls.val_year(params.get('year'))
      
      if 'appleMusicID' in params:
         cls.val_url(params.get('appleMusicID'), True)
      
      if 'deezerID' in params:
         cls.val_deezerId(params.get('deezerID'))
      
      if 'apotifyID' in params:
         cls.val_hashUrl(params.get('apotifyID'))
      
      if 'youTubeID' in params:
         cls.val_hashUrl(params.get('youTubeID'))
      
      if 'youTubeMusicID' in params:
         cls.val_hashUrl(params.get('youTubeMusicID'))
      
      if 'facebookID' in params:
         cls.val_facebookUserProfile(params.get('facebookID'))
      
      if 'instagramID' in params:
         cls.val_username(params.get('instagramID'))
      
      if 'twitterID' in params:
         cls.val_username(params.get('twitterID'))
      
      if 'web' in params:
         cls.val_url(params.get('web'))
      
      if 'color' in params:
         cls.val_hexColor(params.get('color'))
      
      if 'vibrantColor' in params:
         cls.val_hexColor(params.get('vibrantColor'))
   
   
   @classmethod
   def validateUpdateArtist(cls, params: dict):
      """Valida los campos que se pueden actaulizar de un artista
      
      :param `params: dict` — Campos a validar
      """
      if 'tags' in params:
         cls.val_tags(params.get('tags'))
      
      if 'name' in params:
         cls.val_name(params.get('name'))
         
      if 'country' in params:
         cls.val_country_code(params.get('country'))
         
      if 'year' in params:
         cls.val_year(params.get('year'))
      
      if 'appleMusicID' in params:
         cls.val_url(params.get('appleMusicID'), True)
      
      if 'deezerID' in params:
         cls.val_deezerId(params.get('deezerID'))
      
      if 'apotifyID' in params:
         cls.val_hashUrl(params.get('apotifyID'))
      
      if 'youTubeID' in params:
         cls.val_hashUrl(params.get('youTubeID'))
      
      if 'youTubeMusicID' in params:
         cls.val_hashUrl(params.get('youTubeMusicID'))
      
      if 'facebookID' in params:
         cls.val_facebookUserProfile(params.get('facebookID'))
      
      if 'instagramID' in params:
         cls.val_username(params.get('instagramID'))
      
      if 'twitterID' in params:
         cls.val_username(params.get('twitterID'))
      
      if 'web' in params:
         cls.val_url(params.get('web'))
      
      if 'color' in params:
         cls.val_hexColor(params.get('color'))
      
      if 'vibrantColor' in params:
         cls.val_hexColor(params.get('vibrantColor'))
   
   
   @classmethod
   def val_email(cls, email: str):
      'Valida un E-mail'
      if not re.search(EXP_EMAIL, email):
         raise ValidationError(_('Formato de correo electrónico inválido'), 'email')

   
   @classmethod
   def val_year(cls, year: int|str):
      'Valida un año'
      if int(year) > 2023:
         raise ValidationError(_('El año ingresado no es válido'))
   

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
         raise ValidationError(_('El número de teléfono no es válido'), 'cellphone')
      
      
   @classmethod
   def val_tags(cls, tags):
      'Validad el campo de etiquetas'
      if not re.search(EXP_TAGS, tags, re.IGNORECASE):
         raise ValidationError(_('Las etiquetas ingresadas para este campo no tiene el formato correcto'), 'tags')
   
   
   @classmethod
   def val_url(cls, url: str, complete: bool = False):
      'Valida direcciones URL'
      if complete and not re.search(EXP_URL_COMPLETE, url):
         raise ValidationError(_('Dirección URL inválida'), 'url')
      elif not complete and not re.search(EXP_URL, url):
         raise ValidationError(_('Dirección URL inválida'), 'url')
   
   
   @classmethod
   def val_deezerId(cls, id):
      'Valida un ID de Deezer'
      if not re.search(r'^[0-9]+$', id):
         raise ValidationError(_('Id inválido'), 'id')
   
   
   @classmethod
   def val_hashUrl(cls, hash):
      'Valida un hash de una URL'
      if not re.search(EXP_URL_HASH, hash, re.IGNORECASE):
         raise ValidationError(_('Identificador de recurso no válido'), 'id')
   
   
   @classmethod
   def val_facebookUserProfile(cls, username):
      'Valida un hash de una URL de un perfil de facebook'
      if not re.search(EXP_FACEBOOK_PROFILE, username, re.IGNORECASE):
         raise ValidationError(_('Este nombre de usuario no es válido'), 'faecbookID')
   
   
   @classmethod
   def val_hexColor(cls, color):
      'Valida un codigo de color en hexadecimal'
      if not re.search(EXP_COLOR_HEX, color, re.IGNORECASE):
         raise ValidationError(_('Este nombre de usuario no es válido'), 'color')
   
   
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