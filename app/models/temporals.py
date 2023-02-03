from datetime import datetime

from django.db import models

from app.models.artists import Artists
from app.models.lyrics import Lyrics
from app.models.users import Users


class TemporalLyrics(models.Model):
   'Modelo de letras temporales, es decir las que no han sido aprobadas'
   id = models.BigAutoField(primary_key=True)
   name = models.CharField(max_length=80)
   nativeName = models.CharField(max_length=80)
   artistName = models.CharField(max_length=50)
   artist = models.ForeignKey(Artists, on_delete=models.DO_NOTHING, default=None, null=True)
   language  = models.CharField(max_length=10)
   lyric = models.TextField()
   nativeLyric = models.TextField(null=True, default=None)
   sent = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, default=None)
   addedAt = models.DateTimeField(default=datetime.now())
   
   class Meta:
      db_table = "app_temporal_lyrics"
      verbose_name = "tempral lyrics"
      verbose_name_plural = "tempral lyrics"


class TemporalTranslate(models.Model):
   'Modelo de traduciones temporales, es decir las que no han sido aprobadas'
   id = models.BigAutoField(primary_key=True)
   name = models.CharField(max_length=80)
   language = models.CharField(max_length=10)
   translate = models.TextField()
   lyric = models.ForeignKey(Lyrics, on_delete=models.CASCADE)
   sent = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, default=None)
   addedAt = models.DateTimeField(default=datetime.now())
   
   class Meta:
      db_table = "app_temporal_translates"
      verbose_name = "temporal translates"
      verbose_name_plural = "temporal translates"