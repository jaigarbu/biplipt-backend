from datetime import datetime

from django.db import models
from django.utils.translation import gettext as _

from app.models.users import AccountStatus, GenderOptions


class GroupAdmins(models.TextChoices):
   'Opciones para los grupos de los administradores'
   Admin = 1, _('Adminitrador')
   Artist = 2, _('Artista')
   Moderator = 3, _('Moderador')

class NodeTypes(models.TextChoices):
   lyric = 'lyric', _('Letra')
   album = 'album', _('Álbum')
   genre = 'genre', _('Género')
   arits = 'artist', _('Artista')


class Admins(models.Model):
   'Modelo de los administradores'
   id = models.BigAutoField(primary_key=True)
   group = models.CharField(max_length=1, choices=GroupAdmins.choices)
   status = models.CharField(max_length=11, choices=AccountStatus.choices, default=AccountStatus.Unverified)
   verify = models.BooleanField(default=False)
   signature = models.CharField(max_length=255, null=True, default=None)
   name = models.CharField(max_length=20)
   lastName = models.CharField(max_length=30)
   country = models.CharField(max_length=2)
   cellphone = models.CharField(max_length=15, unique=True)
   gender = models.CharField(max_length=1, choices=GenderOptions.choices)
   birthdate = models.DateField()
   email = models.CharField(max_length=50, unique=True)
   password = models.CharField(max_length=255)
   masterKey = models.CharField(max_length=255, null=True, default=None)
   lastSeen = models.DateTimeField(null=True, default=None)
   ip = models.CharField(max_length=15)
   activationKey = models.CharField(max_length=400, null=True, default=None)
   registeredAt = models.DateTimeField(default=datetime.now())
   updatedAt = models.DateTimeField(null=True, default=None)
   
   class Meta:
      verbose_name = "admin"
      verbose_name_plural = "admins"


class AdminsLogin(models.Model):
   'Modelo de resgistro de sessiones de los administradore'
   ssid = models.CharField(max_length=255)
   userAgent = models.CharField(max_length=300)
   loginAt = models.DateTimeField(default=datetime.now())
   ip = models.CharField(max_length=16)
   country = models.CharField(max_length=3)
   aproved = models.BooleanField(default=True)
   admin = models.ForeignKey(Admins, on_delete=models.CASCADE)

   class Meta:
      db_table = 'app_admin_logins'
      verbose_name = "admin login"
      verbose_name_plural = "admin logins"


class ContentMarks(models.Model):
   'Modelo de registro de marcadores de los adminitradores'
   nodeId = models.CharField(max_length=20, db_index=True)
   nodeType = models.CharField(max_length=20, choices=NodeTypes.choices)
   addedAt = models.DateTimeField(default=datetime.now())
   admin = models.ForeignKey(Admins, on_delete=models.CASCADE)

   class Meta:
      db_table = 'app_admin_content_marks'
      verbose_name = "admin mark"
      verbose_name_plural = "admin marks"