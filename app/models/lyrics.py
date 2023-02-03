from datetime import datetime

from django.db import models

from app.models.admins import Admins
from app.models.albums import Albums
from app.models.artists import Artists
from app.models.genres import Genres
from app.models.system import VisibilityOptions
from app.models.users import Users


class Lyrics(models.Model):
   'Modelo de las letras'
   id = models.BigAutoField(primary_key=True)
   dns = models.CharField(max_length=255, db_index=True, unique=True)
   visibility = models.CharField(max_length=10, choices=VisibilityOptions.choices, default=VisibilityOptions.Public)
   verify = models.BooleanField(default=False)
   tags = models.CharField(max_length=255, db_index=True)
   name = models.CharField(max_length=80)
   nativeName = models.CharField(max_length=80)
   track = models.IntegerField(null=True, default=None)
   duraction = models.CharField(max_length=10, null=True, default=None)
   country = models.CharField(max_length=2)
   language = models.CharField(max_length=20)
   year = models.IntegerField(null=True, default=None)
   composers = models.CharField(max_length=255, null=True, default=None)
   writers = models.CharField(max_length=255, null=True, default=None)
   copyright = models.CharField(max_length=400, null=True, default=None)
   lyric = models.TextField()
   nativeLyric = models.TextField(null=True, default=None)
   appleMusicID = models.CharField(max_length=255, null=True, default=None)
   deezerID = models.CharField(max_length=255, null=True, default=None)
   spotifyID = models.CharField(max_length=255, null=True, default=None)
   youTubeID = models.CharField(max_length=255, null=True, default=None)
   youTubeMusicID = models.CharField(max_length=255, null=True, default=None)
   views = models.BigIntegerField(default=0)
   addedAt = models.DateTimeField(default=datetime.now())
   updatedAt = models.DateTimeField(null=True, default=None)
   artist = models.ForeignKey(Artists, on_delete=models.CASCADE)
   album = models.ForeignKey(Albums, on_delete=models.CASCADE)
   genre = models.ForeignKey(Genres, on_delete=models.SET_NULL, null=True)
   approved = models.ForeignKey(Admins, on_delete=models.SET_NULL, null=True)
   sent = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, default=None)
   
   class Meta:
      verbose_name = "lyric"
      verbose_name_plural = "lyrics"


class LyricVersions(models.Model):
   'Modelo de las versiones de las letras'
   id = models.BigAutoField(primary_key=True)
   dns = models.CharField(max_length=255, db_index=True, unique=True)
   visibility = models.CharField(max_length=10, choices=VisibilityOptions.choices, default=VisibilityOptions.Public)
   verify = models.BooleanField(default=False)
   tags = models.CharField(max_length=255, db_index=True)
   name = models.CharField(max_length=80)
   nativeName = models.CharField(max_length=80)
   track = models.IntegerField(null=True, default=None)
   duraction = models.CharField(max_length=10, null=True, default=None)
   country = models.CharField(max_length=2)
   language = models.CharField(max_length=20)
   year = models.IntegerField(null=True, default=None)
   composers = models.CharField(max_length=255, null=True, default=None)
   writers = models.CharField(max_length=255, null=True, default=None)
   copyright = models.CharField(max_length=400, null=True, default=None)
   lyric = models.TextField()
   nativeLyric = models.TextField(null=True, default=None)
   appleMusicID = models.CharField(max_length=255, null=True, default=None)
   deezerID = models.CharField(max_length=255, null=True, default=None)
   spotifyID = models.CharField(max_length=255, null=True, default=None)
   youTubeID = models.CharField(max_length=255, null=True, default=None)
   youTubeMusicID = models.CharField(max_length=255, null=True, default=None)
   views = models.BigIntegerField(default=0)
   addedAt = models.DateTimeField(default=datetime.now())
   updatedAt = models.DateTimeField(null=True, default=None)
   artist = models.ForeignKey(Artists, on_delete=models.CASCADE)
   album = models.ForeignKey(Albums, on_delete=models.CASCADE)
   genre = models.ForeignKey(Genres, on_delete=models.SET_NULL, null=True)
   approved = models.ForeignKey(Admins, on_delete=models.SET_NULL, null=True)
   sent = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, default=None)
   
   class Meta:
      db_table = "app_lyric_versions"
      verbose_name = "lyric version"
      verbose_name_plural = "lyric versions"


class LyricFT(models.Model):
   'Modelo de Feacturing de las letras y de las versiones'
   lyric = models.ForeignKey(Lyrics, on_delete=models.CASCADE)
   name = models.CharField(max_length=80)
   nativeName = models.CharField(max_length=80)
   dns = models.CharField(max_length=255)
   
   class Meta:
      db_table = "app_lyric_ft"
      verbose_name = "lyric featuring"
      verbose_name_plural = "lyrics featuring"


class LyricModified(models.Model):
   'Modelos de registro de modificaciones de las letras'
   lyric = models.ForeignKey(Lyrics, on_delete=models.CASCADE)
   modifiedBy = models.ForeignKey(Admins, on_delete=models.SET_NULL, null=True)
   sent = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, default=None)
   times = models.IntegerField(default=1)
   addedAt = models.DateTimeField(default=datetime.now())
   updatedAt = models.DateTimeField(null=True, default=None)

   class Meta:
      db_table = 'app_lyric_modified'
      verbose_name = "lyric modified"
      verbose_name_plural = "lyrics modified"


class LyricVersionsModified(models.Model):
   'Modelos de registro de modificaciones de las versiones de las letras'
   lyric = models.ForeignKey(LyricVersions, on_delete=models.CASCADE)
   modifiedBy = models.ForeignKey(Admins, on_delete=models.SET_NULL, null=True)
   sent = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, default=None)
   times = models.IntegerField(default=1)
   addedAt = models.DateTimeField(default=datetime.now())
   updatedAt = models.DateTimeField(null=True, default=None)

   class Meta:
      db_table = 'app_lyric_versions_modified'
      verbose_name = "lyric versions modified"
      verbose_name_plural = "lyrics version modified"

   
class LyricLikes(models.Model):
   'Likes de las letras'
   user = models.ForeignKey(Users, on_delete=models.CASCADE)
   lyric = models.ForeignKey(Lyrics, on_delete=models.CASCADE)
   at = models.DateTimeField(default=datetime.now())
   
   class Meta:
      db_table = "app_lyric_likes"
      verbose_name = "lyric likes"
      verbose_name_plural = "lyric likes"
   

class LyricVersionsLikes(models.Model):
   'Likes de las versiones de letras'
   user = models.ForeignKey(Users, on_delete=models.CASCADE)
   lyric = models.ForeignKey(Lyrics, on_delete=models.CASCADE)
   at = models.DateTimeField(default=datetime.now())
   
   class Meta:
      db_table = "app_lyric_verions_likes"
      verbose_name = "lyric versions likes"
      verbose_name_plural = "lyric versions likes"