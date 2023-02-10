import json

from django.utils.translation import activate, get_language_from_request
from django.utils.translation import gettext as _

from app.constants.config import SYSTEM_LANGUAGE
from app.controllers.auth import AuthController
from app.utils.exceptions import HttpError
from core.settings import BASE_DIR


class SystemController:
   
   config = BASE_DIR / 'app/config/app.json';
   locales = BASE_DIR / 'app/config/languages.json';
   
   @classmethod
   def get_system(cls, headers: any):
      """Obtiene la información del sistema
      
      :param `headers: dict` — Headers http de la consulta actual
      """
      try:
         # leer la configuracion del sistema
         with open(cls.config) as jsonfile:
            data: dict = json.load(jsonfile)
         
         with open(cls.locales) as localesfile:
            locales: list = json.load(localesfile)
         
         # Detectar el idioma del navegador del usuario
         userLocale = headers.META.get('HTTP_LANG', None)
         browseLocale = get_language_from_request(headers)
         locale = SYSTEM_LANGUAGE
         if userLocale and userLocale in locales[0]:
            if SYSTEM_LANGUAGE != userLocale:
               locale = userLocale
               activate(locale)
         elif browseLocale in locales[0] and SYSTEM_LANGUAGE != browseLocale:
            locale = browseLocale
            activate(locale)
            
         # Verifica si existe una session iniciada y retornar datos de session
         session = AuthController.validate_session(headers=headers.META)

         return {
            'app': data.get('app'),
            'page': data.get('page'),
            'loggedIn': True if session else False,
            'user': session if session else None,
            'locale': locale,
            'dir': 'ltr',
            'locales': locales[1]
         }
      except FileNotFoundError as e:
         print(e.args)
         raise HttpError(_('Internal Server Error. Please try again later'))