from django.db import models

from app.models.admins import Admin
from app.models.albums import Album
from app.models.artists import Artist
from app.models.genres import Genre
from app.models.system import VisibilityOptions
from app.models.users import User


class Lyric(models.Model):
   'Modelo de las letras'
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
   artist = models.ForeignKey(Artist, on_delete=models.CASCADE, db_column="artistId", related_name="lyrics")
   album = models.ForeignKey(Album, on_delete=models.CASCADE, db_column="albumId", related_name="lyrics")
   genres = models.ManyToManyField(Genre, related_name="lyrics")
   approvedBy = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, db_column="approvedBy", related_name="lyrics")
   sentBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column="sentBy", related_name="lyrics")
   
   class Meta:
      db_table = "lyrics"
      verbose_name = "lyric"
      verbose_name_plural = "lyrics"
   
   def __str__(self):
      return self.title


class LyricFT(models.Model):
   'Modelo de Feacturing de las letras y de las versiones'
   lyric = models.ForeignKey(Lyric, on_delete=models.CASCADE, db_column="lyricId", related_name="ft")
   name = models.CharField(max_length=80)
   nativeName = models.CharField(max_length=80)
   dns = models.CharField(max_length=255, null=True, blank=True)
   
   class Meta:
      db_table = "lyric_ft"
      verbose_name = "lyric featuring"
      verbose_name_plural = "lyrics featuring"
   
   def __str__(self):
      return self.name


class LyricModifications(models.Model):
   'Modelos de registro de modificaciones de las letras'
   lyric = models.ForeignKey(Lyric, on_delete=models.CASCADE, db_column="lyricId", related_name="modifications")
   approvedBy = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, db_column="modifiedBy", related_name="lyricModified")
   sentBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column="sentBy", related_name="lyricModifications")
   times = models.PositiveSmallIntegerField(default=1)
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)

   class Meta:
      db_table = 'lyric_modifications'
      verbose_name = "lyric modifications"
      verbose_name_plural = "lyrics modifications"
   
   def __str__(self):
      return self.lyric.title

   
class LyricLikes(models.Model):
   'Likes de las letras'
   user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="userId", related_name="+")
   lyric = models.ForeignKey(Lyric, on_delete=models.CASCADE, db_column="lyricId", related_name="likes")
   at = models.DateTimeField(auto_now_add=True)
   
   class Meta:
      db_table = "lyric_likes"
      verbose_name = "lyric likes"
      verbose_name_plural = "lyric likes"
   
   def __str__(self):
      return self.lyric.title
