from django.db import models

from app.models.admins import Admin
from app.models.lyrics import Lyric
from app.models.system import VisibilityOptions
from app.models.users import User


class Translate(models.Model):
   'Modelo de las traducciones'
   id = models.BigAutoField(primary_key=True)
   visibility = models.CharField(max_length=10, choices=VisibilityOptions.choices, default=VisibilityOptions.Public)
   lyricId = models.ForeignKey(Lyric, on_delete=models.CASCADE, db_column="lyricId")
   language = models.CharField(max_length=10)
   name = models.CharField(max_length=80)
   lyric = models.TextField()
   sentBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, db_column="sentBy")
   approvedBy = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, db_column="approvedBy")
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)
   
   class Meta:
      db_table = "app_translates"
      verbose_name = "translate"
      verbose_name_plural = "translates"
   
   def __str__(self):
      return self.name


class TranslateModifications(models.Model):
   'Modelo de las modificaciones de las traducciones'
   translateId = models.ForeignKey(Translate, on_delete=models.CASCADE, db_column="translateId")
   approvedBy = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, db_column="approvedBy")
   sentBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, db_column="sentBy")
   times = models.PositiveSmallIntegerField(default=1)
   addedAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)
   
   class Meta:
      db_table = "app_translate_modifications"
      verbose_name = "trasnlate modifications"
      verbose_name_plural = "trasnlate modifications"
   
   def __str__(self):
      return f"translate modified {self.translateId}"