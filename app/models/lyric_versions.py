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
   title = models.CharField(max_length=80)
   nativeTitle = models.CharField(max_length=80)
   track = models.PositiveSmallIntegerField(null=True, blank=True)
   duraction = models.PositiveIntegerField(null=True, blank=True)
   country = models.CharField(max_length=2)
   language = models.CharField(max_length=20)
   year = models.PositiveSmallIntegerField(null=True, blank=True)
   composers = models.CharField(max_length=255, null=True, blank=True)
   writers = models.CharField(max_length=255, null=True, blank=True)
   copyright = models.CharField(max_length=400, null=True, blank=True)
   lyric = models.TextField()
   nativeLyric = models.TextField(null=True, blank=True)
   appleMusicID = models.CharField(max_length=255, null=True, blank=True)
   deezerID = models.CharField(max_length=255, null=True, blank=True)
   spotifyID = models.CharField(max_length=255, null=True, blank=True)
   youTubeID = models.CharField(max_length=255, null=True, blank=True)
   youTubeMusicID = models.CharField(max_length=255, null=True, blank=True)
   views = models.BigIntegerField(default=0)
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)
   lyric = models.ForeignKey(Lyric, on_delete=models.CASCADE, db_column="lyricId", related_name="versions")
   artist = models.ForeignKey(Artist, on_delete=models.CASCADE, db_column="artistId", related_name="lyricVersions")
   album = models.ForeignKey(Album, on_delete=models.CASCADE, db_column="albumId", related_name="lyricVersions")
   genres = models.ManyToManyField(Genre, related_name="lyricVersions")
   approvedBy = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, db_column="approvedBy", related_name="lyricVersions")
   sentBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column="sentBy", related_name="lyricVersions")
      
   class Meta:
      db_table = "lyric_versions"
      verbose_name = "lyric versions"
      verbose_name_plural = "lyric versions"
   
   def __str__(self):
      return self.name


class LyricVersionsModifications(models.Model):
   'Modelos de registro de modificaciones de las versiones de las letras'
   lyric = models.ForeignKey(LyricVersions, on_delete=models.CASCADE, db_column="lyricId", related_name="modifications")
   approvedBy = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, db_column="modifiedBy", related_name="lyricVersionsModified")
   sentBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, db_column="sentBy", related_name="lyricVersionsModified")
   times = models.PositiveSmallIntegerField(default=1)
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)

   class Meta:
      db_table = 'lyric_versions_modifications'
      verbose_name = "lyric versions modifications"
      verbose_name_plural = "lyrics version modifications"
   
   def __str__(self):
      return self.lyric.title


class LyricVersionLikes(models.Model):
   'Likes de las versiones de letras'
   user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="userId", related_name="lyricVersionsLikes")
   lyric = models.ForeignKey(LyricVersions, on_delete=models.CASCADE, db_column="lyricId", related_name="likes")
   at = models.DateTimeField(auto_now_add=True)
   
   class Meta:
      db_table = "lyric_verion_likes"
      verbose_name = "lyric version likes"
      verbose_name_plural = "lyric version likes"
   
   def __str__(self):
      return self.lyric.title