from django.db import models
from django.utils.translation import gettext as _

from app.models.admins import Admin
from app.models.artists import Artist
from app.models.genres import Genre
from app.models.system import VisibilityOptions


class AlbumType(models.TextChoices):
   'Tipos de albumes'
   album = 'album', _('Álbum')
   single = 'single', _('Sencillo')


class Album(models.Model):
   'Modelo de los álbumes'
   id = models.BigAutoField(primary_key=True)
   dns = models.CharField(max_length=255, db_index=True, unique=True)
   visibility = models.CharField(max_length=10, choices=VisibilityOptions.choices, default=VisibilityOptions.Public)
   verify = models.BooleanField(default=False)
   tags = models.CharField(max_length=255)
   name = models.CharField(max_length=80)
   nativeName = models.CharField(max_length=80)
   type = models.CharField(max_length=6, choices=AlbumType.choices)
   country = models.CharField(max_length=2)
   year = models.IntegerField(null=True, default=None)
   number = models.IntegerField(null=True, default=None)
   language = models.CharField(max_length=20)
   appleMusicID = models.CharField(max_length=255, null=True, default=None)
   deezerID = models.CharField(max_length=255, null=True, default=None)
   spotifyID = models.CharField(max_length=255, null=True, default=None)
   youTubeID = models.CharField(max_length=255, null=True, default=None)
   youTubeMusicID = models.CharField(max_length=255, null=True, default=None)
   cover = models.CharField(max_length=80)
   coverSD = models.CharField(max_length=80)
   color = models.CharField(max_length=9)
   vibrantColor = models.CharField(max_length=9)
   views = models.BigIntegerField(default=0)
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)
   genres = models.ManyToManyField(Genre, related_name="genres")
   artistId = models.ForeignKey(Artist, on_delete=models.CASCADE, db_column="artistId")
   addedBy = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, db_column="addedBy")
   
   class Meta:
      db_table = "app_albums"
      verbose_name = "album"
      verbose_name_plural = "albums"
   
   def __str__(self):
      return self.name
   

class AlbumFT(models.Model):
   'Modelo de Feacturing de los álbumes'
   albumId = models.ForeignKey(Album, on_delete=models.CASCADE, db_column="albumId")
   name = models.CharField(max_length=80)
   nativeName = models.CharField(max_length=80)
   dns = models.CharField(max_length=255)
   
   class Meta:
      db_table = 'app_album_ft'
      verbose_name = "album featuring"
      verbose_name_plural = "album featuring"
   
   def __str__(self):
      return self.name


class AlbumModifications(models.Model):
   'Modelos de registro de modificaciones de los artistas'
   albumId = models.ForeignKey(Album, on_delete=models.CASCADE, db_column="albumId")
   modifiedBy = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, default=None, db_column="modifiedBy")
   times = models.PositiveSmallIntegerField(default=1)
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)

   class Meta:
      db_table = 'app_album_modifications'
      verbose_name = "album modifications"
      verbose_name_plural = "album modifications"
   
   def __str__(self):
      return f"modified album: {self.albumId}"