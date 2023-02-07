from django.db import models

from app.models.artists import Artist
from app.models.lyrics import Lyric
from app.models.users import User


class TemporalLyric(models.Model):
   'Modelo de letras temporales, es decir las que no han sido aprobadas'
   id = models.BigAutoField(primary_key=True)
   name = models.CharField(max_length=80)
   nativeName = models.CharField(max_length=80)
   artistName = models.CharField(max_length=50)
   artist = models.ForeignKey(Artist, on_delete=models.DO_NOTHING, default=None, null=True)
   language  = models.CharField(max_length=10)
   lyric = models.TextField()
   nativeLyric = models.TextField(null=True, default=None)
   sentBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, db_column="sentBy")
   addedAt = models.DateTimeField(auto_now_add=True)
   
   class Meta:
      db_table = "app_temporal_lyrics"
      verbose_name = "tempral lyrics"
      verbose_name_plural = "tempral lyrics"
   
   def __str__(self):
      return self.name


class TemporalTranslate(models.Model):
   'Modelo de traduciones temporales, es decir las que no han sido aprobadas'
   id = models.BigAutoField(primary_key=True)
   name = models.CharField(max_length=80)
   language = models.CharField(max_length=10)
   translate = models.TextField()
   lyric = models.ForeignKey(Lyric, on_delete=models.CASCADE)
   sentBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, db_column="sentBy")
   addedAt = models.DateTimeField(auto_now_add=True)
   
   class Meta:
      db_table = "app_temporal_translates"
      verbose_name = "temporal translates"
      verbose_name_plural = "temporal translates"
   
   def __str__(self):
      return self.name