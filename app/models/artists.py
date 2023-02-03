from datetime import datetime

from django.db import models
from django.utils.translation import gettext as _

from app.models.admins import Admins
from app.models.genres import Genres
from app.models.system import VisibilityOptions
from app.models.users import Users


class ArtistsCategory(models.TextChoices):
   'Categorias de los artistas'
   Band = 'band', _('Banda')
   Chorister = 'choir', _('Corista')
   Composer = 'composer', _('Compositor')
   dj = 'DJ', _("DJ's")
   Group = 'group', _('Grupo')
   Instrumentalist = 'instrumentalist', _('Instrumentalista')
   Musician = 'musician', _('Músico')
   Orchestra = 'orchestra', _('Orquesta')
   Other = 'other', _('Otra categoría')
   Producer = 'producer', _('Produtor')
   Rapper = 'rapper', _('Rapero')
   Singer = 'singer', _('Solista')
   

class Artists(models.Model):
   'Modelo de los artistas'
   id = models.BigAutoField(primary_key=True)
   dns = models.CharField(max_length=255, db_index=True, unique=True)
   visibility = models.CharField(max_length=10, choices=VisibilityOptions.choices, default=VisibilityOptions.Public)
   verify = models.BooleanField(default=False)
   tags = models.CharField(max_length=255)
   name = models.CharField(max_length=80)
   nativeName = models.CharField(max_length=80)
   type = models.CharField(max_length=15, choices=ArtistsCategory.choices)
   country = models.CharField(max_length=2)
   year = models.IntegerField(null=True, default=None)
   appleMusicID = models.CharField(max_length=255, null=True, default=None)
   deezerID = models.CharField(max_length=255, null=True, default=None)
   spotifyID = models.CharField(max_length=255, null=True, default=None)
   youTubeID = models.CharField(max_length=255, null=True, default=None)
   youTubeMusicID = models.CharField(max_length=255, null=True, default=None)
   facebookID = models.CharField(max_length=255, null=True, default=None)
   instagramID = models.CharField(max_length=255, null=True, default=None)
   twitterID = models.CharField(max_length=255, null=True, default=None)
   web = models.CharField(max_length=100, null=True, default=None)
   photo = models.CharField(max_length=80)
   cover = models.CharField(max_length=80)
   color = models.CharField(max_length=9)
   vibrantColor = models.CharField(max_length=9)
   views = models.BigIntegerField(default=0)
   info = models.CharField(max_length=250, null=True, default=None)
   addedAt = models.DateTimeField(default=datetime.now())
   updatedAt = models.DateTimeField(null=True, default=None)
   genre = models.ForeignKey(Genres, on_delete=models.SET_NULL, null=True)
   addedBy = models.ForeignKey(Admins, on_delete=models.SET_NULL, null=True)
   
   class Meta:
      verbose_name = "artist"
      verbose_name_plural = "artists"


class ArtistImages(models.Model):
   'Modelo de la galeria de imágenes de los artistas'
   artist = models.ForeignKey(Artists, on_delete=models.CASCADE)
   image = models.CharField(max_length=80)
   addedAt = models.DateTimeField(default=datetime.now())
   updatedAt = models.DateTimeField(null=True, default=None)
   admin = models.ForeignKey(Admins, on_delete=models.SET_DEFAULT, null=True, default=None)
   user = models.ForeignKey(Users, on_delete=models.SET_DEFAULT, null=True, default=None)

   class Meta:
      db_table = 'app_artist_images'
      verbose_name = "artist image"
      verbose_name_plural = "artist images"


class ArtistModified(models.Model):
   'Modelos de registro de modificaciones de los artistas'
   artist = models.ForeignKey(Artists, on_delete=models.CASCADE)
   modifiedBy = models.ForeignKey(Admins, on_delete=models.SET_DEFAULT, null=True, default=None)
   times = models.IntegerField(default=1)
   addedAt = models.DateTimeField(default=datetime.now())
   updatedAt = models.DateTimeField(null=True, default=None)

   class Meta:
      db_table = 'app_artist_modified'
      verbose_name = "artist modified"
      verbose_name_plural = "artists modified"