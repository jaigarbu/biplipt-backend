from django.db import models

from app.models.admins import Admin
from app.models.albums import Album
from app.models.artists import Artist
from app.models.genres import Genre
from app.models.lyrics import Lyric
from app.models.system import VisibilityOptions
from app.models.users import User


class LyricVersions(models.Model):
   'Modelo de las versiones de las letras'
   id = models.BigAutoField(primary_key=True)
   dns = models.CharField(max_length=255, db_index=True, unique=True)
   visibility = models.CharField(max_length=10, choices=VisibilityOptions.choices, default=VisibilityOptions.Public)
   verify = models.BooleanField(default=False)
   tags = models.CharField(max_length=255, db_index=True)
   name = models.CharField(max_length=80)
   nativeName = models.CharField(max_length=80)
   track = models.PositiveSmallIntegerField(null=True, default=None)
   duraction = models.PositiveIntegerField(null=True, default=None)
   country = models.CharField(max_length=2)
   language = models.CharField(max_length=20)
   year = models.PositiveSmallIntegerField(null=True, default=None)
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
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)
   lyricId = models.ForeignKey(Lyric, on_delete=models.CASCADE, db_column="lyricId")
   artistId = models.ForeignKey(Artist, on_delete=models.CASCADE, db_column="artistId")
   albumId = models.ForeignKey(Album, on_delete=models.CASCADE, db_column="albumId")
   genresList = models.ManyToManyField(Genre, related_name="genresList")
   approvedBy = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, db_column="approvedBy")
   sentBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, db_column="sentBy")
   
   class Meta:
      db_table = "app_lyric_versions"
      verbose_name = "lyric versions"
      verbose_name_plural = "lyric versions"
   
   def __str__(self):
      return self.name


class LyricVersionsModifications(models.Model):
   'Modelos de registro de modificaciones de las versiones de las letras'
   lyricId = models.ForeignKey(LyricVersions, on_delete=models.CASCADE, db_column="lyricId")
   modifiedBy = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, db_column="modifiedBy")
   sentBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, db_column="sentBy")
   times = models.PositiveSmallIntegerField(default=1)
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)

   class Meta:
      db_table = 'app_lyric_versions_modifications'
      verbose_name = "lyric versions modifications"
      verbose_name_plural = "lyrics version modifications"
   
   def __str__(self):
      return f"version modified: {self.lyricId}"


class LyricVersionLikes(models.Model):
   'Likes de las versiones de letras'
   userId = models.ForeignKey(User, on_delete=models.CASCADE, db_column="userId")
   lyricId = models.ForeignKey(LyricVersions, on_delete=models.CASCADE, db_column="lyricId")
   at = models.DateTimeField(auto_now_add=True)
   
   class Meta:
      db_table = "app_lyric_verion_likes"
      verbose_name = "lyric version likes"
      verbose_name_plural = "lyric version likes"
   
   def __str__(self):
      return f"like to: {self.lyricId}"