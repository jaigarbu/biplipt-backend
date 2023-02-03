from datetime import datetime

from django.db import models

from app.models.admins import Admins
from app.models.lyrics import Lyrics
from app.models.system import VisibilityOptions
from app.models.users import Users


class Translates(models.Model):
   'Modelo de las traducciones'
   id = models.BigAutoField(primary_key=True)
   visibility = models.CharField(max_length=10, choices=VisibilityOptions.choices, default=VisibilityOptions.Public)
   lyric = models.ForeignKey(Lyrics, on_delete=models.CASCADE)
   language = models.CharField(max_length=10)
   name = models.CharField(max_length=80)
   lyric = models.TextField()
   sent = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, default=None)
   approvedBy = models.ForeignKey(Admins, on_delete=models.SET_NULL, null=True)
   addedAt = models.DateTimeField(default=datetime.now())
   updatedAt = models.DateTimeField(null=True, default=None)
   
   class Meta:
      verbose_name = "translates"
      verbose_name_plural = "translates"


class TranslatesModified(models.Model):
   'Modelo de las modificaciones de las traducciones'
   translate = models.ForeignKey(Translates, on_delete=models.CASCADE)
   approvedBy = models.ForeignKey(Admins, on_delete=models.SET_NULL, null=True)
   sent = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, default=None)
   times = models.IntegerField(default=1)
   addedAt = models.DateTimeField(default=datetime.now())
   updatedAt = models.DateTimeField(null=True, default=None)
   
   class Meta:
      db_table = "app_translates_modified"
      verbose_name = "trasnlates modified"
      verbose_name_plural = "trasnlates modified"