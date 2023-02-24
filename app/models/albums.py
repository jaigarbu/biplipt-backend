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
   year = models.IntegerField(null=True, blank=True)
   number = models.IntegerField(null=True, blank=True)
   language = models.CharField(max_length=20)
   appleMusicID = models.CharField(max_length=255, null=True, blank=True)
   deezerID = models.CharField(max_length=255, null=True, blank=True)
   spotifyID = models.CharField(max_length=255, null=True, blank=True)
   youTubeID = models.CharField(max_length=255, null=True, blank=True)
   youTubeMusicID = models.CharField(max_length=255, null=True, blank=True)
   cover = models.CharField(max_length=80, null=True, blank=True)
   coverSD = models.CharField(max_length=80, null=True, blank=True)
   color = models.CharField(max_length=9, null=True, blank=True)
   vibrantColor = models.CharField(max_length=9, null=True, blank=True)
   views = models.BigIntegerField(default=0)
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)
   genres = models.ManyToManyField(Genre, related_name="albums")
   artist = models.ForeignKey(Artist, on_delete=models.CASCADE, db_column="artistId", related_name="albums")
   addedBy = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, db_column="addedBy", related_name="albumsAdded")
   
   class Meta:
      db_table = "albums"
      verbose_name = "album"
      verbose_name_plural = "albums"
   
   def __str__(self):
      return self.name
   

class AlbumFT(models.Model):
   'Modelo de Feacturing de los álbumes'
   album = models.ForeignKey(Album, on_delete=models.CASCADE, db_column="albumId", related_name="ft")
   name = models.CharField(max_length=80)
   nativeName = models.CharField(max_length=80)
   dns = models.CharField(max_length=255, null=True, blank=True)
   
   class Meta:
      db_table = 'album_ft'
      verbose_name = "album featuring"
      verbose_name_plural = "album featuring"
   
   def __str__(self):
      return self.name


class AlbumModifications(models.Model):
   'Modelos de registro de modificaciones de los artistas'
   album = models.ForeignKey(Album, on_delete=models.CASCADE, db_column="albumId", related_name="modifications")
   modifiedBy = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, db_column="modifiedBy", related_name="albumsModified")
   times = models.PositiveSmallIntegerField(default=1)
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)

   class Meta:
      db_table = 'album_modifications'
      verbose_name = "album modifications"
      verbose_name_plural = "album modifications"
   
   def __str__(self):
      return self.album.name