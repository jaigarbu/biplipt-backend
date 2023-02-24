from django.db import models
from django.utils.translation import gettext as _

from app.models.admins import Admin
from app.models.genres import Genre
from app.models.system import VisibilityOptions
from app.models.users import User


class ArtistCategories(models.TextChoices):
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
   

class Artist(models.Model):
   'Modelo de los artistas'
   id = models.BigAutoField(primary_key=True)
   dns = models.CharField(max_length=255, db_index=True, unique=True)
   visibility = models.CharField(max_length=10, choices=VisibilityOptions.choices, default=VisibilityOptions.Public)
   verify = models.BooleanField(default=False)
   tags = models.CharField(max_length=255)
   name = models.CharField(max_length=80)
   nativeName = models.CharField(max_length=80)
   type = models.CharField(max_length=15, choices=ArtistCategories.choices)
   country = models.CharField(max_length=2)
   year = models.IntegerField(null=True, blank=True)
   appleMusicID = models.CharField(max_length=255, null=True, blank=True)
   deezerID = models.CharField(max_length=255, null=True, blank=True)
   spotifyID = models.CharField(max_length=255, null=True, blank=True)
   youTubeID = models.CharField(max_length=255, null=True, blank=True)
   youTubeMusicID = models.CharField(max_length=255, null=True, blank=True)
   facebookID = models.CharField(max_length=255, null=True, blank=True)
   instagramID = models.CharField(max_length=255, null=True, blank=True)
   twitterID = models.CharField(max_length=255, null=True, blank=True)
   web = models.CharField(max_length=100, null=True, blank=True)
   photo = models.CharField(max_length=80, null=True, blank=True)
   cover = models.CharField(max_length=80, null=True, blank=True)
   color = models.CharField(max_length=9, null=True, blank=True)
   vibrantColor = models.CharField(max_length=9, null=True, blank=True)
   views = models.BigIntegerField(default=0)
   info = models.CharField(max_length=250, null=True, blank=True)
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)
   genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, db_column="genreId", related_name="artists")
   addedBy = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, db_column="addedBy", related_name="artistsAdded")
   images = models.ManyToManyField("ArtistImages", related_name="artitsImages", blank=True)
   
   class Meta:
      db_table = "artists"
      verbose_name = "artist"
      verbose_name_plural = "artists"
   
   def __str__(self):
      return self.name


class ArtistImages(models.Model):
   'Modelo de la galeria de imágenes de los artistas'
   id = models.BigAutoField(primary_key=True)
   image = models.CharField(max_length=80)
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)
   admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True, db_column="adminId", related_name="imagesAdded")
   user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column="userId", related_name="imagesAdded")

   class Meta:
      db_table = 'artist_images'
      verbose_name = "artist image"
      verbose_name_plural = "artist images"
   
   def __str__(self):
      return self.image


class ArtistModifications(models.Model):
   'Modelos de registro de modificaciones de los artistas'
   artist = models.ForeignKey(Artist, on_delete=models.CASCADE, db_column="artistId", related_name="modifications")
   modifiedBy = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, db_column="modifiedBy", related_name="artistsModified")
   times = models.PositiveSmallIntegerField(default=1)
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)

   class Meta:
      db_table = 'artist_modifications'
      verbose_name = "artist modifications"
      verbose_name_plural = "artist modifications"
   
   def __str__(self):
      return self.artist.name