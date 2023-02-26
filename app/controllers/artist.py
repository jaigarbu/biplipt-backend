from datetime import datetime

import shortuuid
from django.db.models import F
from django.utils import timezone
from django.utils.translation import gettext as _

from app.controllers.auth import AuthController
from app.controllers.genre import GenreController
from app.controllers.validations import ValidationsController
from app.functions.chars import normalize_string
from app.models.admins import Admin
from app.models.artists import Artist, ArtistModifications
from app.models.genres import Genre
from app.utils.exceptions import HttpError


class ArtistController:
   """Controlador de los artistas"""
   
   offset = 0
   limit = 10
   artistNotExists = _('Lo sentimos el artista ingresado no existe')
   artistAlreadyExists = _('Lo sentimos el artista %s ya se encuentra en nuestra base de datos')
   
   @classmethod
   def getArtist(cls, field: str, value: any, headers: dict) -> Artist:
      """Consulta un artista y lo retorna
      
      :param `field: str` — Campo por el que se va a buscar al artista
      :param `value: any` — Valor para la busqueda
      :param `headers: dict` — Headers http de la consulta actual
      :return — Artist
      """
      # Establecer session actual para efectos de la busqueda
      session = AuthController.validate_session(headers)
      
      try:
         if field == 'id':
            ValidationsController.val_id(value)
            artist = Artist.objects.get(id=value)
            AuthController.validate_permissions(session, artist.visibility)
         elif field == "dns":
            ValidationsController.val_dns(value)
            artist = Artist.objects.get(dns=value)
            AuthController.validate_permissions(session, artist.visibility)
         elif field == 'name':
            ValidationsController.val_name(value)
            artist = Artist.objects.get(name=value)
            AuthController.validate_permissions(session, artist.visibility)
         else:
            raise HttpError(cls.artistNotExists, 404)
         return artist
      except Artist.DoesNotExist:
         raise HttpError(cls.artistNotExists, 404)
   
   
   @classmethod
   def getArtists(cls, headers: dict, orderBy: str=None, offset: int=None, limit: int=None):
      """Retorna una lista de artistas
      
      :param `headers: dict` — Headers http de la consulta actual
      :param `orderBy: str` — Orden para mostrar los resultados. Default `None`
      :param `offset: int` — Posicion de inicio de la consulta en la base de datos. Default `None`
      :param `limit: int` — Limite de resultados. Default `None`
      """
      # Configurar obciones de consulta
      order = ValidationsController.set_queryOrderBy(orderBy)
      minimun = offset if offset else cls.offset
      maximun = limit if limit else cls.limit
      
      # Establecer session actual para validar permisos de visualizacion
      session = AuthController.validate_session(headers)
      
      # Buscar en la base de datos teniendo en cuenta los permisos de visualizacion
      if AuthController.val_allow(session, 1):
         artists = Artist.objects.all().order_by(order)[minimun:maximun]
         return artists
      
      if AuthController.val_allow(session, 5):
         artists = Artist.objects.all().exclude(visibility='block').order_by(order)[minimun:maximun]
         return artists
      
      artists = Artist.objects.filter(visibility='public').order_by(order)[minimun:maximun]
      return artists
   
   
   @classmethod
   def createArtist(cls, inputs: dict, headers: dict) -> Artist:
      """Inserta un artista en la base de datos
      
      :param `inputs: dict` — Datos necesarios para la creacion del artista
      :param `headers: dict` — Headers http de la consulta actual
      :return — Artist
      """
      # Valdar session actual y permisos para crear el artista
      session = AuthController.validate_session(headers)
      if not AuthController.val_allow(session, 5):
         raise HttpError(AuthController.unauthorized, 401)
      
      # Validar campos para la creacion de artista
      ValidationsController.validateRegisterArtist(params=inputs)
      
      # Normalizacion de los datos de busqueda para control de seguridad
      name = normalize_string(inputs.get('name'), 'title')
      nativeName = inputs.get('nativeName') if 'nativeName' in inputs else name
      dns = shortuuid.uuid()
      
      try:
         # Verificar que no exista el artista en la base de datos
         artist = Artist.objects.filter(name=name, nativeName=nativeName).exists()
         if artist:
            raise HttpError(cls.artistAlreadyExists % name, 400)
         
         # Validar informacion del administrador o moderador actual
         admin = Admin.objects.get(id=session.get('id'))
         if admin.status != 'active':
            raise HttpError(AuthController.unauthorized, 401)
         
         # comprobar existencia del genero
         genre = Genre.objects.get(id=inputs.get('genre'))
         
         # Preparacion de la consulta
         inputs['dns'] = dns
         inputs['genre'] = genre
         inputs['name'] = name
         inputs['nativeName'] = nativeName
         inputs['type'] = inputs.get('type').value
         inputs['visibility'] = inputs.get('visibility').value
         inputs['addedBy'] = admin
         
         # Creacion del artista en la base de datos
         newArtist = Artist.objects.create(**inputs)
         return newArtist
      except Admin.DoesNotExist:
         raise HttpError(AuthController.unauthorized, 401)
      except Genre.DoesNotExist:
         raise HttpError(GenreController.genreNotExist, 401)
   
   
   @classmethod
   def updateArtist(cls, dns: str, inputs: dict, headers: dict) -> Artist:
      """Actualiza un artista en la base de datos
      
      :param `dns: str` — DNS del artista a editar
      :param `inputs: dict` — Campos que seran editados
      :param `headers: dict` — Headers http de la consulta actual
      :return — Artist
      """      
      # Comprobar session actual para verificar permisos
      session = AuthController.validate_session(headers)
      if not AuthController.val_allow(payload=session, group=5):
         raise HttpError(AuthController.unauthorized, 401)
      
      # Validar los datos que se van a modificar
      ValidationsController.validateUpdateArtist(params=inputs)
      
      try:
         # Verificar existencia y validez de cuenta de administracion
         admin = Admin.objects.get(id=session.get('id'))
         if admin.status != 'active':
            raise HttpError(AuthController.unauthorized, 401)
         
         # Verificar existencia del artista a modificar y preparar la consulta
         artist = Artist.objects.get(dns=dns)
         for key, value in inputs.items():
            setattr(artist, key, value)
         artist.updatedAt = datetime.now(tz=timezone.utc)
         artist.save()
         
         # Registrar el cambio actual
         cls.setRegisterUpdated(artist, admin)
         
         return artist
      except Admin.DoesNotExist:
         raise HttpError(AuthController.unauthorized, 401)
      except Artist.DoesNotExist:
         raise HttpError(cls.artistNotExists, 404)
   
   
   @classmethod
   def setRegisterUpdated(cls, artist: Artist, modifier: Admin):
      """Registra una modificacion en la tabla de historial de modificaciones de artistas
      
      :param `artist: Artist` — Artista modificado
      :param `modifier: Admin` — Adminitrador modificador
      """      
      modification = ArtistModifications.objects.filter(artist=artist.id, modifiedBy=modifier.id).exists()
      if modification:
         ArtistModifications.objects.filter(
            artist=artist.id, 
            modifiedBy=modifier.id
         ).update(
            times=F('times')+1, 
            updatedAt=datetime.now(tz=timezone.utc)
         )
      else:
         ArtistModifications.objects.create(artist=artist, modifiedBy=modifier)