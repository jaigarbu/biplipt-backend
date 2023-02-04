from django.db.models import Q
from django.utils.translation import gettext as _

from app.constants.config import JWS_KEY
from app.controllers.auth import AuthController
from app.controllers.validations import ValidationsController
from app.functions.chars import normalize_string
from app.models.genres import Genres
from app.utils.exceptions import HttpError


class GenreController:
   
   offset = 0
   limit = 10
   genreNotExist = _('El género no existe')
   genreAlreadyExist = _('El género ya existe')
   genreRestricted = _('Lo sentimos este género está restringido')
   
   
   @classmethod
   def getGenre(cls, field: str, value: any, headers: any):
      """Consulta un género de la base de datos
      
      :param `field: str` — Campo por el que se buscará el género
      :param `value: any` — Valor por el que se buscará el género
      :param `headers: any` — Encabezados GraphQL de la consulta actual
      :return — User
      """
      # Verificar si existe session activa para efectos de modos de buscar información en base de datos
      token = headers.get('HTTP_AUTHORIZATION', None)
      session = AuthController.verifyJWSToken(key=JWS_KEY, token=token)
      
      try:
         if field == 'id':
            ValidationsController.val_id(value)
            genre = Genres.objects.get(ID=value)
            cls._validate_permissions(session, genre.visibility)
         elif field == 'dns':
            ValidationsController.val_dns(value)
            genre = Genres.objects.get(DNS=value)
            cls._validate_permissions(session, genre.visibility)
         elif field == "name":
            ValidationsController.val_name(value)
            genre = Genres.objects.get(name=value)
            cls._validate_permissions(session, genre.visibility)
         else:
            raise HttpError(cls.genreNotExist, 400)
         return genre
      except Genres.DoesNotExist:
         raise HttpError(cls.genreNotExist, 400)
   
   
   @classmethod
   def getGenres(cls, headers: dict, orderBy: str|None=None, offset: int|None=None, limit: int|None=None):
      # establecer el orden de la consulta
      if orderBy != None:
         line = orderBy.value.partition('_')
         order = line[0] if line[2] == "ASC" else f'-{line[0]}'
      else:
         order = 'ID'
      minimun = offset if offset != None else cls.offset
      maximun = limit if limit != None else cls.limit
      
      # Validar persimos de usuario para visaulizacion de datos
      token = headers.get('HTTP_AUTHORIZATION', None)
      session = AuthController.validate_session(token)
      
      if isinstance(session, dict):
         if ValidationsController.val_allow(session, 1):
            genres = Genres.objects.all().order_by(order)[minimun:maximun]
            return genres
            
         if ValidationsController.val_allow(session, 5):
            genres = Genres.objects.all().exclude(visibility='block').order_by(order)[minimun:maximun]
            return genres
         
         if ValidationsController.val_allow(session, 4):
            genres = Genres.objects.filter(visibility='public').all().order_by(order)[minimun:maximun]
            return genres
      else:
         genres = Genres.objects.filter(visibility='public').all().order_by(order)[minimun:maximun]
         return genres
   
   
   @classmethod
   def createGenre(cls, inputs: dict, headers: any) -> Genres:
      """Crea un genero en la base de datos
      
      :param `inputs: dict` — Campos requeridos para la creacion del genero
      :param `headers: any` — Headers Http de la consulta actual
      :return — Genre
      """
      # Validar campos
      ValidationsController.val_name(inputs.get('name'))
      
      # Prerarcion de consulta y normlización
      dns = normalize_string(inputs.get('name'), 'url')
      name = normalize_string(inputs.get('name'), 'name')
      
      # verificar si ya existe el genero
      genre = Genres.objects.filter(name=name).exists()
      if genre:
         raise HttpError(cls.genreAlreadyExist, 400)
      
      # crear el genero
      newGnere = Genres.objects.create(
         dns=dns,
         name=name,
         visibility=inputs.get('visibility').value[0],
         addedBy_id=inputs.get('addedBy')
      )
      return newGnere
   
   
   @classmethod
   def _validate_permissions(cls, session: dict|bool, visibility: str):
      if visibility == 'block' and not ValidationsController.val_allow(session, 1):
         raise HttpError(cls.genreNotExist, 404)
            
      if visibility == 'private' and not ValidationsController.val_allow(session, 6):
         raise HttpError(cls.genreNotExist, 404)
            
      if visibility == 'restricted' and not ValidationsController.val_allow(session, 5):
         raise HttpError(cls.genreRestricted, 404)

