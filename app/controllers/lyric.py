from django.utils.translation import gettext as _

from app.controllers.token import TokenController
from app.controllers.validations import ValidationsController
from app.models.lyrics import Lyrics
from app.utils.exceptions import HttpError


class LyricController:
   
   lyricNotExist = _('La letra solicitada no existe')
   lyricRestricted = _('La letra solicitada está restringida')
   
   
   @classmethod
   def getLyric(cls, field: str, value: any, headers: any):
      """Obtiene una letra
      
      :param `field: str` — Campo por el que se buscará la letra
      :param `value: any` — valor a buscar
      :param `headers: any` — Headers de la consulta
      """
      # Determinar session activa para permisos de usuario. Permite filtrar datos ocutos o restringidos
      token = headers.get('HTTP_AUTHORIZATION', None)
      session = TokenController.verifyJWSToken(token=token)
         
      try:
         # validacion de campos de busqueda
         if field == 'id':
            ValidationsController.val_id(value)
            lyric = Lyrics.objects.get(id=value)
            cls._validate_permissions(session, lyric.visibility)
         elif field == 'dns':
            lyric = Lyrics.objects.get(dns=value)
            ValidationsController.val_dns(value)
            cls._validate_permissions(session, lyric.visibility)
         else:
            raise HttpError(cls.lyricNotExist, 404)
         return lyric
      except Lyrics.DoesNotExist:
         raise HttpError(cls.lyricNotExist, 404)

         
      
         
   @classmethod
   def _validate_permissions(cls, session: dict|bool, visibility: str):
      if visibility == 'block' and not ValidationsController.val_allow(session, 1):
         raise HttpError(cls.lyricNotExist, 404)
            
      if visibility == 'private' and not ValidationsController.val_allow(session, 6):
         raise HttpError(cls.lyricNotExist, 404)
            
      if visibility == 'restricted' and not ValidationsController.val_allow(session, 5):
         raise HttpError(cls.lyricRestricted, 404)