from datetime import datetime

from django.db import models
from django.utils.translation import gettext as _

from app.models.admins import Admins
from app.models.artists import Artists
from app.models.genres import Genres
from app.models.system import VisibilityOptions


class AlbumType(models.TextChoices):
   'Tipos de albumes'
   album = 'album', _('Álbum')
   single = 'single', _('Sencillo')


class Albums(models.Model):
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
   addedAt = models.DateTimeField(default=datetime.now())
   updatedAt = models.DateTimeField(null=True, default=None)
   genre = models.ForeignKey(Genres, on_delete=models.SET_NULL, null=True)
   artist = models.ForeignKey(Artists, on_delete=models.CASCADE)
   addedBy = models.ForeignKey(Admins, on_delete=models.SET_NULL, null=True)
   
   class Meta:
      verbose_name = "album"
      verbose_name_plural = "albums"
   

class AlbumFT(models.Model):
   'Modelo de Feacturing de los álbumes'
   album = models.ForeignKey(Albums, on_delete=models.CASCADE)
   name = models.CharField(max_length=80)
   nativeName = models.CharField(max_length=80)
   dns = models.CharField(max_length=255)
   
   class Meta:
      db_table = 'app_album_ft'
      verbose_name = "album featuring"
      verbose_name_plural = "album featurings"


class AlbumModified(models.Model):
   'Modelos de registro de modificaciones de los artistas'
   album = models.ForeignKey(Albums, on_delete=models.CASCADE)
   modifiedBy = models.ForeignKey(Admins, on_delete=models.SET_NULL, null=True, default=None)
   times = models.IntegerField(default=1)
   addedAt = models.DateTimeField(default=datetime.now())
   updatedAt = models.DateTimeField(null=True, default=None)

   class Meta:
      db_table = 'app_album_modified'
      verbose_name = "album modified"
      verbose_name_plural = "albums modified"