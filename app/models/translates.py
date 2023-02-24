from django.db import models

from app.models.admins import Admin
from app.models.lyrics import Lyric
from app.models.system import VisibilityOptions
from app.models.users import User


class Translate(models.Model):
   'Modelo de las traducciones'
   id = models.BigAutoField(primary_key=True)
   visibility = models.CharField(max_length=10, choices=VisibilityOptions.choices, default=VisibilityOptions.Public)
   lyric = models.ForeignKey(Lyric, on_delete=models.CASCADE, db_column="lyricId", related_name="trasnlates")
   language = models.CharField(max_length=10)
   title = models.CharField(max_length=80)
   lyric = models.TextField()
   sentBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column="sentBy", related_name="translates")
   approvedBy = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, db_column="approvedBy", related_name="lyricsTranslates")
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)
   
   class Meta:
      db_table = "translates"
      verbose_name = "translate"
      verbose_name_plural = "translates"
   
   def __str__(self):
      return self.title


class TranslateModifications(models.Model):
   'Modelo de las modificaciones de las traducciones'
   translate = models.ForeignKey(Translate, on_delete=models.CASCADE, db_column="translateId", related_name="modifications")
   approvedBy = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, db_column="approvedBy", related_name="translatesModified")
   sentBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, db_column="sentBy", related_name="translatesModified")
   times = models.PositiveSmallIntegerField(default=1)
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)
   
   class Meta:
      db_table = "translate_modifications"
      verbose_name = "trasnlate modifications"
      verbose_name_plural = "trasnlate modifications"
   
   def __str__(self):
      return self.translate.title