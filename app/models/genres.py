from django.db import models

from app.models.admins import Admin
from app.models.system import VisibilityOptions


class Genre(models.Model):
   'Modelo de los géneros'
   id = models.BigAutoField(primary_key=True)
   dns = models.CharField(max_length=255, unique=True)
   visibility = models.CharField(max_length=10, choices=VisibilityOptions.choices)
   name = models.CharField(max_length=30)
   addedBy = models.ForeignKey(Admin, null=True, on_delete=models.SET_NULL, db_column="addedBy", related_name="genresAdded")
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)
      
   class Meta:
      db_table = "genres"
      verbose_name = "genre"
      verbose_name_plural = "genres"
   
   def __str__(self):
      return self.name


class GenreModifications(models.Model):
   'Modelo de registro de cambios de los generos'
   genre = models.ForeignKey(Genre, on_delete=models.CASCADE, db_column="genreId", related_name="modifications")
   modifier = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, db_column="modifierId", related_name="genresModificated")
   times = models.PositiveSmallIntegerField(default=1)
   modifiedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)
   
   class Meta:
      db_table = 'genre_modifications'
      verbose_name = "genre modifications"
      verbose_name_plural = "genres modifications"
   
   def __str__(self) -> str:
      return self.genre