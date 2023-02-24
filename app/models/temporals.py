from django.db import models

from app.models.artists import Artist
from app.models.lyrics import Lyric
from app.models.users import User


class TemporalLyric(models.Model):
   'Modelo de letras temporales, es decir las que no han sido aprobadas'
   id = models.BigAutoField(primary_key=True)
   title = models.CharField(max_length=80)
   nativeTitle = models.CharField(max_length=80)
   artistName = models.CharField(max_length=50)
   artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True, blank=True)
   language  = models.CharField(max_length=10)
   lyric = models.TextField()
   nativeLyric = models.TextField(null=True, blank=True)
   sentBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column="sentBy", related_name="temporalLyrics")
   addedAt = models.DateTimeField(auto_now_add=True)
   
   class Meta:
      db_table = "temporal_lyrics"
      verbose_name = "tempral lyrics"
      verbose_name_plural = "tempral lyrics"
   
   def __str__(self):
      return self.title


class TemporalTranslate(models.Model):
   'Modelo de traduciones temporales, es decir las que no han sido aprobadas'
   id = models.BigAutoField(primary_key=True)
   title = models.CharField(max_length=80)
   language = models.CharField(max_length=10)
   translate = models.TextField()
   lyric = models.ForeignKey(Lyric, on_delete=models.CASCADE, db_column="lyricId", related_name="+")
   sentBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column="sentBy", related_name="translatesPending")
   addedAt = models.DateTimeField(auto_now_add=True)
   
   class Meta:
      db_table = "temporal_translates"
      verbose_name = "temporal translates"
      verbose_name_plural = "temporal translates"
   
   def __str__(self):
      return self.title