from datetime import datetime

import shortuuid
from django.db.models import F
from django.utils import timezone
from django.utils.translation import gettext as _

from app.controllers.artist import ArtistController
from app.controllers.auth import AuthController
from app.controllers.uploads import UploadsController
from app.controllers.validations import ValidationsController
from app.functions.chars import normalize_string
from app.models.admins import Admin
from app.models.albums import Album, AlbumFT, AlbumModifications
from app.models.artists import Artist
from app.utils.exceptions import HttpError


class AlbumController:
   'Controlador de los álbumes'
   
   offset = 0
   limit = 10
   albumNotExists = _('Lo sentimos, el álbum ingresado no existe en nuestra base de datos')
   albumAlreadyExits = _('Lo sentimos, el álbum %s ya existe en el artista %s')
   
   @classmethod
   def getAlbum(cls, field: str, value: int|str, headers: dict) -> Album:
      """Cnsulta y retorna un álbum
      
      :param `field: str` — Campo por el que se va a buscar al álbum
      :param `value: any` — Valor de busqueda
      :param `headers: dict` — Headers http de la consulta actual
      :return — Album
      """      
      # Determinar session activa para permisos de usuario. Permite filtrar datos ocultos o restringidos
      session = AuthController.validate_session(headers)
         
      try:
         # validacion de campos de busqueda y realizar la busqueda en base de datos
         if field == 'id':
            ValidationsController.val_id(value)
            album = Album.objects.get(id=value)
            AuthController.validate_permissions(session, album.visibility)
         elif field == 'dns':
            ValidationsController.val_dns(value)
            album = Album.objects.get(dns=value)
            AuthController.validate_permissions(session, album.visibility)
         else:
            raise HttpError(cls.albumNotExists, 404)
         return album
      except Album.DoesNotExist:
         raise HttpError(cls.albumNotExists, 404)
   
   
   @classmethod
   def getAlbums(cls, headers: dict, orderBy: str|None=None, offset: int|None=None, limit: int|None=None):
      """Consulta y retorna una lista de álbumes
      
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
            albums = Album.objects.all().order_by(order)[minimun:maximun]
            return albums
         
         if AuthController.val_allow(session, 5):
            albums = Album.objects.all().exclude(visibility="block").order_by(order)[minimun:maximun]
            return albums
      
      albums = Album.objects.filter(visibility="public").order_by(order)[minimun:maximun]
      return albums
   
   
   @classmethod
   def createAlbum(cls, inputs: dict, headers: dict) -> Album:
      # Validar session actual y verificar permisos para crear álbumes
      session = AuthController.validate_session(headers)
      if not AuthController.val_allow(payload=session, group=5):
         raise HttpError(AuthController.unauthorized, 401)
      
      # Validar campos necesarios para creacion de letras
      ValidationsController.validateRegisterAlbum(inputs)
      
      # Normalizacion de los datos de busqueda
      name = normalize_string(inputs['name'], 'title')
      nativeName = inputs['nativeName'] if 'nativeName' in inputs else name
      dns = shortuuid.uuid()
      
      try:
         # Verificar la existencia del administrador que va a aprovar o ingresar este recurso
         admin = Admin.objects.get(id=session['id'])
         if admin.status != 'active':
            raise HttpError(AuthController.unauthorized, 401)
         
         # Verificar existencia del artista y control de integridad, verifica que el álbum no exista
         artist = Artist.objects.get(dns=inputs['artist'])
         album = Album.objects.filter(name=name, artist=artist.id).exists()
         if album:
            raise HttpError(cls.albumAlreadyExits % (name, artist.name), 400)
         
         # Configuracion y guardado de imagen de álbum en caso de existir
         if 'cover' in inputs:
            fileName = UploadsController.saveAlbumCover(file=inputs['cover'])
            inputs['cover'] = fileName
         
         # Preparar la consulta con los campos obligatorios
         inputs['dns'] = dns
         inputs['name'] = name
         inputs['nativeName'] = nativeName
         inputs['artist'] = artist
         inputs['visibility'] = inputs['visibility'].value
         inputs['type'] = inputs['type'].value
         inputs['addedBy'] = admin
         
         # Lipieza y configuarcion de campos que requieren procesos adicionales
         genres = inputs['genres']
         ft = inputs.get('ft')
         inputs.pop('genres')
         if 'ft' in inputs:
            inputs.pop('ft')
         
         # Crear el album en la base de datos
         newAlbum = Album.objects.create(**inputs)
         
         # registrar featuring del álbum si existen
         if ft:
            cls.setFeaturing(ft, newAlbum)
         
         # Registrar géneros del álbum
         
         return newAlbum
      except Artist.DoesNotExist:
         raise HttpError(ArtistController.artistNotExists, 404)
      except Admin.DoesNotExist: # type: ignore
         raise HttpError(AuthController.unauthorized, 401)
   
   
   @classmethod
   def updateAlbum(cls, dns: str, inputs: dict, headers: dict):
      pass
   
   
   @classmethod
   def deleteAlbum(cls, id: int, headers: dict):
      pass
   
   
   @classmethod
   def setFeaturing(cls, ft: list, album: Album):
      """Registra el Featuring de un album
      
      :param `ft: list` — Lista de featuring
      :param `album: Album` — Álbum a registrar ft
      """ 
      # Construir Iterbale de creacion para bulk de django
      ouputBulk = []
      for item in ft:
         item['name'] = normalize_string(item['name'], 'title')
         item['nativeName'] = item['nativeName'] if 'nativeName' in item else item['name']
         ouputBulk.append(AlbumFT(album=album, **item))
      AlbumFT.objects.bulk_create(ouputBulk)
   
   
   @classmethod
   def setRegisterUpdated(cls, album: Album, modifier: Admin):
      """Registra una modificacion en la tabla de historial de modificaciones de álbumes
      
      :param `genre: Genre` — Álbum modificado
      :param `modifier: Admin` — Adminitrador modificador
      """      
      modification = AlbumModifications.objects.filter(album=album.id, modifiedBy=modifier.id).exists()
      if modification:
         AlbumModifications.objects.filter(
            album=album.id, 
            modifier=modifier.id,
         ).update(
            times=F('times')+1, 
            updatedAt=datetime.now(tz=timezone.utc)
         )
      else:
         AlbumModifications.objects.create(album=album, modifiedBy=modifier)