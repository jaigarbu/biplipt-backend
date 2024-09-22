from datetime import datetime

import shortuuid
from django.db.models import F
from django.utils import timezone
from django.utils.translation import gettext as _

from app.controllers.album import AlbumController
from app.controllers.artist import ArtistController
from app.controllers.auth import AuthController
from app.controllers.validations import ValidationsController
from app.functions.chars import normalize_string
from app.models.admins import Admin
from app.models.albums import Album
from app.models.artists import Artist
from app.models.lyrics import Lyric, LyricModifications
from app.models.users import User
from app.utils.exceptions import HttpError


class LyricController:
   'Controlador de las letras'
   
   offset = 0
   limit = 10
   lyricNotExist = _('Lo sentimos, la letra solicitada no existe')
   lyricRestricted = _('Lo sentimos, la letra solicitada está restringida')
   lyricAlreadyExist = _('Lo sentimos, la letra %s ya se encuentra registrada en el álbum del artista actual')
   
   
   @classmethod
   def getLyric(cls, field: str, value: any, headers: dict):
      """Obtiene una letra
      
      :param `field: str` — Campo por el que se buscará la letra
      :param `value: any` — valor a buscar
      :param `headers: dict` — Headers de la consulta
      """
      # Determinar session activa para permisos de usuario. Permite filtrar datos ocultos o restringidos
      session = AuthController.validate_session(headers)
         
      try:
         # validacion de campos de busqueda y realizar la busqueda en base de datos
         if field == 'id':
            ValidationsController.val_id(value)
            lyric = Lyric.objects.get(id=value)
            AuthController.validate_permissions(session, lyric.visibility)
         elif field == 'dns':
            ValidationsController.val_dns(value)
            lyric = Lyric.objects.get(dns=value)
            AuthController.validate_permissions(session, lyric.visibility)
         else:
            raise HttpError(cls.lyricNotExist, 404)
         return lyric
      except Lyric.DoesNotExist:
         raise HttpError(cls.lyricNotExist, 404)
   
   
   @classmethod
   def getLyrics(cls,  headers: dict, orderBy: str=None, offset: int=None, limit: int=None):
      """Consulta y retorna una lista de letras
      
      :param `headers: dict` — Headers http de la consulta actual
      :param `orderBy: str | None` — Orden de los resultados. Default `None`
      :param `offset: int | None` — Inicio de la consulta. Default `None`
      :param `limit: int | None` — Limite de resultados. Default `None`
      """
      # Establecer el orden, offset y limite de la consulta
      order = ValidationsController.set_queryOrderBy(orderBy)
      minimun = offset if offset != None else cls.offset
      maximun = limit if limit != None else cls.limit
      
      # Determina session actual para filtrado de datos
      session = AuthController.validate_session(headers=headers)
      
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
   def createLyric(cls, inputs: dict, headers: dict) -> Lyric:
      """Crea una letra en la base de datos publica
      
      :param `inputs: dict` — Campos necesarios para crear una letra
      :param `headers: dict` — Headers http de la consulta actual
      :return -- Lyric
      """
      # Validar session actual y verificar permisos para crear letras
      session = AuthController.validate_session(headers)
      if not AuthController.val_allow(payload=session, group=5):
         raise HttpError(AuthController.unauthorized, 401)
      
      # Validar campos necesarios para creacion de letras
      ValidationsController.validateRegisterLyric(inputs)
      
      # Normalizacion de los datos de busqueda
      title = normalize_string(inputs['title'], 'title')
      nativeTitle = inputs['nativeTitle'] if 'nativeTitle' in inputs else title
      dns = shortuuid.uuid(pad_length=32)
      
      try:
         # Verificar la existencia del administrador que va a aprovar o ingresar esta letra
         admin = Admin.objects.get(id=session['id'])
         if admin.status != 'active':
            raise HttpError(AuthController.unauthorized, 401)
         
         # Verificar existencia del artista y el album en la base de datos
         artist = Artist.objects.get(dns=inputs['artist'])
         album = Album.objects.get(dns=inputs['album'])
                  
         # Control de integridad, verificar que la letra no exista en el album del artista
         lyric = Lyric.objects.filter(title=title, album=album.id, artist=artist.id).exists()
         if lyric:
            raise HttpError(cls.lyricAlreadyExist % inputs['title'], 400)
         
         # Veridicar si hay un usuario vinculado a la letra como enviador del recurso
         user = User.objects.filter(id=inputs['sentBy']).first()
         
         # Prepara la consulta de creacion de letra
         inputs['dns'] = dns
         inputs['album'] = album
         inputs['artist'] = artist
         inputs['sentBy'] = user
         inputs['approvedBy'] = admin
         inputs['visibility'] = inputs.get('visibility').value
         
         
      except Artist.DoesNotExist:
         raise HttpError(ArtistController.artistNotExists, 404)
      except Album.DoesNotExist:
         raise HttpError(AlbumController.albumNotExits, 404)
      except Admin.DoesNotExist:
         raise HttpError(AuthController.unauthorized, 401)
   
   
   @classmethod
   def updateLyric(cls, dns: str, inputs: dict, headers: dict):
      pass
   
   
   @classmethod
   def deleteLyric(cls, id: str, headers: dict):
      pass
   
   
   @classmethod
   def setRegisterUpdated(cls, lyric: Lyric, modifier: Admin, sender: User=None):
      """Registra una modificacion en la tabla de historial de modificaciones de letras
      
      :param `genre: Genre` — Letra modificada
      :param `modifier: Admin` — Adminitrador modificador
      :param `sender: User | None` — AUsuario que envió la letra
      """      
      modification = LyricModifications.objects.filter(lyric=lyric.id, approvedBy=modifier.id).exists()
      if modification:
         LyricModifications.objects.filter(
            lyric=lyric.id, 
            modifier=modifier.id,
         ).update(
            times=F('times')+1, 
            updatedAt=datetime.now(tz=timezone.utc)
         )
      else:
         LyricModifications.objects.create(lyric=lyric, approvedBy=modifier, sentBy=sender)