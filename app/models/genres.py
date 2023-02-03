from datetime import datetime

from django.db import models

from app.models.admins import Admins
from app.models.system import VisibilityOptions


class Genres(models.Model):
   'Modelo de los géneros'
   id = models.BigAutoField(primary_key=True)
   dns = models.CharField(max_length=255, unique=True)
   visibility = models.CharField(max_length=10, choices=VisibilityOptions.choices)
   name = models.CharField(max_length=30)
   addedBy = models.ForeignKey(Admins, null=True, on_delete=models.SET_NULL)
   addedAt = models.DateTimeField(default=datetime.now())
   updatedAt = models.DateTimeField(null=True, default=None)
      
   class Meta:
      verbose_name = "genre"
      verbose_name_plural = "genres"


class GenreModified(models.Model):
   'Modelo de registro de cambios de los generos'
   genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
   modifiedBy = models.ForeignKey(Admins, on_delete=models.CASCADE)
   times = models.CharField(max_length=10)
   modifiedAt = models.DateTimeField(default=datetime.now())
   updatedAt = models.DateTimeField(null=True)
   
   class Meta:
      db_table = 'app_genre_modified'
      verbose_name = "genre modified"
      verbose_name_plural = "genres modified"