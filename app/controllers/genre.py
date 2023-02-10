from django.utils.translation import gettext as _

from app.controllers.auth import AuthController
from app.controllers.validations import ValidationsController
from app.functions.chars import normalize_string
from app.models.admins import Admin
from app.models.genres import Genre
from app.utils.exceptions import HttpError


class GenreController:
   
   offset = 0
   limit = 10
   genreNotExist = _('El género no existe')
   genreAlreadyExist = _('El género ya existe')
   genreRestricted = _('Lo sentimos este género está restringido')
   
   
   @classmethod
   def getGenre(cls, field: str, value: any, headers: dict):
      """Consulta un género de la base de datos
      
      :param `field: str` — Campo por el que se buscará el género
      :param `value: any` — Valor por el que se buscará el género
      :param `headers: dict` — Encabezados GraphQL de la consulta actual
      :return — User
      """
      # Verificar si existe session activa para efectos de modos de buscar información en base de datos
      session = AuthController.validate_session(headers=headers)
      
      try:
         if field == 'id':
            ValidationsController.val_id(value)
            genre = Genre.objects.get(id=value)
            cls._validate_permissions(session, genre.visibility)
         elif field == 'dns':
            ValidationsController.val_dns(value)
            genre = Genre.objects.get(dns=value)
            cls._validate_permissions(session, genre.visibility)
         elif field == "name":
            ValidationsController.val_name(value)
            genre = Genre.objects.get(name=value)
            cls._validate_permissions(session, genre.visibility)
         else:
            raise HttpError(cls.genreNotExist, 400)
         return genre
      except Genre.DoesNotExist:
         raise HttpError(cls.genreNotExist, 400)
   
   
   @classmethod
   def getGenres(cls, headers: dict, orderBy: any = None, offset: int|None=None, limit: int|None=None):
      """Obtiene varios géneros
      
      :param `headers: dict` — Headers http de la consulta actual
      :param `orderBy: str | None` — Orden de los resultados optenidos. Default `None`
      :param `offset: int | None` — Posicion de inicio de la consulta. Default `None`
      :param `limit: int | None` — Limite de resultados. Default `None`
      :return — List
      """      
      # establecer el orden de la consulta
      if orderBy != None:
         line = orderBy.value.partition('_')
         order = line[0] if line[2] == "asc" else f'-{line[0]}'
      else:
         order = 'id'
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
      
      genres = Genre.objects.filter(visibility='public').all().order_by(order)[minimun:maximun]
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
      dns = normalize_string(inputs.get('name'), 'url')
      name = normalize_string(inputs.get('name'), 'name')
      
      try:
         # verificar si ya existe el genero
         genre = Genre.objects.filter(name=name).exists()
         if genre:
            raise HttpError(cls.genreAlreadyExist, 400)

         # verificar existencia de administrador (requerido por el modelo)
         admin = Admin.objects.get(id=session.get('id'))

         # crear el genero
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
   def deleteGenre(cls, id: any, headers: dict):
      """Elimina un genero de la base de datos
      
      :param `id: any` — Id del género a eliminar
      :param `headers: dict` — Headers Http de la consulta actual
      """
      # determinar session actual y validar permiso de eliminiacion
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
   def _validate_permissions(cls, session: dict|bool, visibility: str):
      if visibility == 'block' and not AuthController.val_allow(session, 1):
         raise HttpError(cls.genreNotExist, 404)
            
      if visibility == 'private' and not AuthController.val_allow(session, 6):
         raise HttpError(cls.genreNotExist, 404)
            
      if visibility == 'restricted' and not AuthController.val_allow(session, 5):
         raise HttpError(cls.genreRestricted, 404)

