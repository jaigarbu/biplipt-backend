from datetime import datetime

import shortuuid
from django.db.models import F
from django.utils import timezone
from django.utils.translation import gettext as _

from app.controllers.auth import AuthController
from app.controllers.validations import ValidationsController
from app.functions.chars import normalize_string
from app.models.admins import Admin
from app.models.genres import Genre, GenreModifications
from app.utils.exceptions import HttpError


class GenreController:
   """Controlador de los géneros
   
   :raises `HttpError` — Excepcion para errores HTTP internos
   """   
   
   offset = 0
   limit = 10
   genreNotExist = _('Lo sentimos el género ingresado no existe')
   genreAlreadyExist = _('Lo sentimos el género %s ya existe')
   
   
   @classmethod
   def getGenre(cls, field: str, value: any, headers: dict):
      """Consulta un género de la base de datos
      
      :param `field: str` — Campo por el que se buscará el género
      :param `value: any` — Valor por el que se buscará el género
      :param `headers: dict` — Encabezados GraphQL de la consulta actual
      :return — User
      """
      # Verificar si existe session activa para efectos de modos de buscar la información en base de datos
      session = AuthController.validate_session(headers=headers)
      
      try:
         if field == 'id':
            ValidationsController.val_id(value)
            genre = Genre.objects.get(id=value)
            AuthController.validate_permissions(session, genre.visibility)
         elif field == 'dns':
            ValidationsController.val_dns(value)
            genre = Genre.objects.get(dns=value)
            AuthController.validate_permissions(session, genre.visibility)
         elif field == "name":
            ValidationsController.val_name(value)
            genre = Genre.objects.get(name=value)
            AuthController.validate_permissions(session, genre.visibility)
         else:
            raise HttpError(cls.genreNotExist, 400)
         return genre
      except Genre.DoesNotExist:
         raise HttpError(cls.genreNotExist, 400)
   
   
   @classmethod
   def getGenres(cls, headers: dict, orderBy: str=None, offset: int|None=None, limit: int|None=None):
      """Obtiene una lista de géneros
      
      :param `headers: dict` — Headers http de la consulta actual
      :param `orderBy: str | None` — Orden de los resultados optenidos. Default `None`
      :param `offset: int | None` — Posicion de inicio de la consulta. Default `None`
      :param `limit: int | None` — Limite de resultados. Default `None`
      :return — List
      """      
      # establecer el orden de la consulta
      order = ValidationsController.set_queryOrderBy(orderBy)
      minimun = offset if offset != None else cls.offset
      maximun = limit if limit != None else cls.limit
      
      # Validar persimos de usuario para visaulizacion de datos
      session = AuthController.validate_session(headers=headers)
      
      # Consultar en base de datos de acuerdo a los permisos
      if AuthController.val_allow(session, 1):
         genres = Genre.objects.all().order_by(order)[minimun:maximun]
         return genres
         
      if AuthController.val_allow(session, 5):
         genres = Genre.objects.all().exclude(visibility='block').order_by(order)[minimun:maximun]
         return genres
      
      genres = Genre.objects.filter(visibility='public').order_by(order)[minimun:maximun]
      return genres
   
   
   @classmethod
   def createGenre(cls, inputs: dict, headers: dict) -> Genre:
      """Crea un genero en la base de datos
      
      :param `inputs: dict` — Campos requeridos para la creacion del genero
      :param `headers: any` — Headers Http de la consulta actual
      :return — Genre
      """
      # comprobar session actual y validar permisos
      session = AuthController.validate_session(headers=headers)
      if not AuthController.val_allow(payload=session, group=5):
         raise HttpError(AuthController.unauthorized, 401)
      
      # Validar campos
      ValidationsController.val_name(inputs.get('name'))
      
      # Preparación de consulta y normlización
      dns = shortuuid.uuid()
      name = normalize_string(inputs.get('name'), 'title')
      
      try:
         # verificar que no exista el género en base de datos
         genre = Genre.objects.filter(name=name).exists()
         if genre:
            raise HttpError(cls.genreAlreadyExist % name, 400)
         
         # Validar la informacion del adminitrador o moderador actual
         admin = Admin.objects.get(id=session.get('id'))
         if admin.status != 'active':
            raise HttpError(AuthController.unauthorized, 401)
         
         # Creacion del género en la base de datos
         newGnere = Genre.objects.create(
            dns=dns,
            name=name,
            visibility=inputs.get('visibility').value,
            addedBy=admin
         )
         return newGnere
      except Admin.DoesNotExist:
         raise HttpError(AuthController.unauthorized, 401)
   
   
   @classmethod
   def updateGenre(cls, dns: str, inputs: dict, headers: dict) -> Genre:
      """Actualiza un género en la base de datos
      
      :param `dns: str` — DNS del género a actualizar
      :param `inputs: dict` — Campos a actualizar
      :param `headers: dict` — Headers http de la consulta actual
      :return — Genre
      """      
      # comprobar session actual y validar permisos
      session = AuthController.validate_session(headers=headers)
      if not AuthController.val_allow(payload=session, group=5):
         raise HttpError(AuthController.unauthorized, 401)
      
      try:
         # verificar permisos del adminstrador para poder editar
         admin = Admin.objects.get(id=session.get('id'))
         if admin.status != 'active':
            raise HttpError(AuthController.unauthorized, 401)
         
         # verificar la existencia del genero a modificar y comprobar cambios
         # ValidationsController.val_dns(dns)
         genre = Genre.objects.get(dns=dns)
         if 'name' in inputs or 'visibility' in inputs:
            name = normalize_string(inputs.get('name'), 'title') if 'name' in inputs else genre.name
            visibility = inputs.get('visibility').value if 'visibility' in inputs else genre.visibility

            if name != genre.name or visibility != genre.visibility:
               genre.name = name
               genre.visibility = visibility
               genre.updatedAt = datetime.now(tz=timezone.utc)
               genre.save()
               cls.setRegisterUpdated(genre, admin)
               
         return genre
      except Admin.DoesNotExist:
         raise HttpError(AuthController.unauthorized, 401)
      except Genre.DoesNotExist:
         raise HttpError(cls.genreNotExist, 404)
   
   
   @classmethod
   def deleteGenre(cls, id: any, headers: dict):
      """Elimina un genero de la base de datos
      
      :param `id: any` — Id del género a eliminar
      :param `headers: dict` — Headers Http de la consulta actual
      """
      # Determinar session actual y validar permiso de eliminiacion
      session = AuthController.validate_session(headers=headers)
      if not AuthController.val_allow(payload=session, group=1):
         raise HttpError(AuthController.unauthorized, 401)
      
      try:
         # comprobar validez de id y la existencia del genero a eliminar
         ValidationsController.val_id(id=id)
         genre = Genre.objects.get(id=id)
         genre.delete()
         return True
      except Genre.DoesNotExist:
         raise HttpError(cls.genreNotExist, 404)


   @classmethod
   def setRegisterUpdated(cls, genre: Genre, modifier: Admin):
      """Registra una modificacion en la tabla de historial de modificaciones de género
      
      :param `genre: Genre` — Género modificado
      :param `modifier: Admin` — Adminitrador modificador de género
      """      
      modification = GenreModifications.objects.filter(genre=genre.id, modifier=modifier.id).exists()
      if modification:
         GenreModifications.objects.filter(
            genre=genre.id, 
            modifier=modifier.id
         ).update(
            times=F('times')+1, 
            updatedAt=datetime.now(tz=timezone.utc)
         )
      else:
         GenreModifications.objects.create(genre=genre, modifier=modifier)