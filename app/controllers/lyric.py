from django.utils.translation import gettext as _

from app.controllers.auth import AuthController
from app.controllers.validations import ValidationsController
from app.models.lyrics import Lyric
from app.utils.exceptions import HttpError


class LyricController:
   
   offset = 0
   limit = 10
   lyricNotExist = _('La letra solicitada no existe')
   lyricRestricted = _('La letra solicitada está restringida')
   
   
   @classmethod
   def getLyric(cls, field: str, value: any, headers: dict):
      """Obtiene una letra
      
      :param `field: str` — Campo por el que se buscará la letra
      :param `value: any` — valor a buscar
      :param `headers: dict` — Headers de la consulta
      """
      # Determinar session activa para permisos de usuario. Permite filtrar datos ocultos o restringidos
      session = AuthController.validate_session(headers)
         
      # validacion de campos de busqueda y realizar la busqueda en base de datos
      # y comprobar los permisos necesarios para tal consulta y disponibilidad
      try:
         if field == 'id':
            ValidationsController.val_id(value)
            lyric = Lyric.objects.get(id=value)
            cls._validate_permissions(session, lyric.visibility)
         elif field == 'dns':
            lyric = Lyric.objects.get(dns=value)
            ValidationsController.val_dns(value)
            cls._validate_permissions(session, lyric.visibility)
         else:
            raise HttpError(cls.lyricNotExist, 404)
         return lyric
      except Lyric.DoesNotExist:
         raise HttpError(cls.lyricNotExist, 404)
   
   
   @classmethod
   def getLyrics(cls,  headers: dict, orderBy: str|None=None, offset: int|None=None, limit: int|None=None):
      """Obtiene los generos desiponibles en basse de datos
      
      :param `headers: dict` — Headers http de la consulta actual
      :param `orderBy: str | None` — Orden de los resultados. Default `None`
      :param `offset: int | None` — Inicio de la consulta. Default `None`
      :param `limit: int | None` — Limite de resultados. Default `None`
      """
      # determinar session activa para permisos de usuario. Permite filtrar datos ocultos o restringidos
      session = AuthController.validate_session(headers=headers)
      
      # valaidar y establecer el orderBy, offset y limit de la consulta
      order = ValidationsController.set_queryOrderBy(orderBy)
      minimun = offset if offset != None else cls.offset
      maximun = limit if limit != None else cls.limit
      
      # realizar la consulta considerando lo sfiltros disponibles
      if isinstance(session, dict):
         if AuthController.val_allow(session, 1):
            lyrics = Lyric.objects.all().order_by(order)[minimun:maximun]
            return lyrics
         
         if AuthController.val_allow(session, 5):
            lyrics = Lyric.objects.all().exclude(visibility="block").order_by(order)[minimun:maximun]
            return lyrics
      
      lyrics = Lyric.objects.filter(visibility="public").order_by(order)[minimun:maximun]
      return lyrics
      

   @classmethod
   def _validate_permissions(cls, session: dict|bool, visibility: str):
      if visibility == 'block' and not AuthController.val_allow(session, 1):
         raise HttpError(cls.lyricNotExist, 404)
            
      if visibility == 'private' and not AuthController.val_allow(session, 6):
         raise HttpError(cls.lyricNotExist, 404)
            
      if visibility == 'restricted' and not AuthController.val_allow(session, 5):
         raise HttpError(cls.lyricRestricted, 404)