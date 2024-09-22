import hashlib
import os
import time

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext as _

from app.constants.config import IMAGE_EXTENSION
from app.controllers.validations import ValidationsController
from app.utils.exceptions import HttpError
from core.settings import BASE_DIR


class UploadsController:
   'Controlador para la carga de archivos en el servidor'
   
   albumsCoverPath = BASE_DIR / 'storage/albums/'
   artistCoverPath = BASE_DIR / 'storage/artist/covers/'
   artistPhotosPath = BASE_DIR / 'storage/artist/photos/'
   
   
   @classmethod
   def validate_requirements(cls, file: InMemoryUploadedFile, type: str):
      """Valida los requerimientos minimos para la carga de un archivo
      
      :param `file: InMemoryUploadedFile` — Archivo a validar
      :param `type: str` — Tipo de archivo a validar
      """      
      if type == "img":
         ValidationsController.val_file_extension(file.content_type, 'img')
         ValidationsController.val_file_size(file.size, 'img')
      elif type == "album":
         ValidationsController.val_file_extension(file.content_type, 'img')
         ValidationsController.val_file_size(file.size, 'album')
   
   
   @classmethod
   def rename_file(cls, file: InMemoryUploadedFile, type: str='img') -> str:
      """Renombra un archivo
      
      :param `file: InMemoryUploadedFile` — Archivo a renombrar
      :param `type: str` — Tipo de archivo o relacion en el sistema. Default `'img'`
      :return — str
      """
      # Detectar y establecer le extension del archivo
      extension = IMAGE_EXTENSION.get(file.content_type, None)
      if not extension:
         raise HttpError(_('Archivo no válido'), 400)
      
      # Determinar algoritmo para garantizar autenticidad y renombrar archivo
      if type == "img":
         baseName = str(time.time()).encode()
         hash = hashlib.sha1(baseName).hexdigest()
         name = hash + extension
      elif type == 'photo':
         name = InMemoryUploadedFile.name
      else:
         name = InMemoryUploadedFile.name
      return name
   
   
   @classmethod
   def validateUnique(cls, path: str) -> bool:
      """Valida la existencia de un archivo en el path espeficicado
      
      :param `path: str` — Path para bsucar el archivo
      :return — bool
      """
      return os.path.exists(path)
   
   
   @classmethod
   def save_file(cls, file: InMemoryUploadedFile, path: str) -> bool:
      """Guarda un archivo en el path especificado
      
      :param `file: InMemoryUploadedFile` — Archivo en memoria que será guardado
      :param `path: str` — Ruta par guardar el archivo
      :return — bool
      """
      try:
         bytes = file.read()
         with open(path, 'wb') as f:
            f.write(bytes)
         return True
      except FileNotFoundError:
         return False

   
   @classmethod
   def saveAlbumCover(cls, file: InMemoryUploadedFile):
      # Comprobar requerimeintos del archivo
      cls.validate_requirements(file, 'album')
      fileName = cls.rename_file(file, 'img')
      
      # Comprobar la no existencia del archivo y renombrar archivo en memoria
      path = os.path.join(cls.albumsCoverPath, fileName)
      control=0
      while cls.validateUnique(path):
         fileName = cls.rename_file(file, 'img')
         control = control+1
         if control > 3:
            break
      file.name = fileName
      
      # Guardar el archivo
      success = cls.save_file(file, path)
      if not success:
         raise HttpError(_('No fue posible cargar el archivo en nuestro sistema'), 500)
      return fileName
      