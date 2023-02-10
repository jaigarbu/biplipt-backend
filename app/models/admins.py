from django.db import models
from django.utils.translation import gettext as _

from app.models.system import AccountStatus, GenderOptions


class GroupAdmins(models.TextChoices):
   'Opciones para los grupos de los administradores'
   Admin = '1', _('Adminitrador')
   Artist = '2', _('Artista')
   Moderator = '3', _('Moderador')

class NodeTypes(models.TextChoices):
   lyric = 'lyric', _('Letra')
   album = 'album', _('Álbum')
   genre = 'genre', _('Género')
   arits = 'artist', _('Artista')


class Admin(models.Model):
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
   registeredAt = models.DateTimeField(auto_now_add=True)
   updatedAt = models.DateTimeField(auto_now=True)
   
   class Meta:
      db_table = "app_admin"
      verbose_name = "admin"
      verbose_name_plural = "admins"
   
   def __str__(self):
      return self.name


class AdminsLogin(models.Model):
   'Modelo de resgistro de sessiones de los administradores'
   ssid = models.CharField(max_length=255)
   userAgent = models.CharField(max_length=300)
   loginAt = models.DateTimeField(auto_now_add=True)
   ip = models.CharField(max_length=16)
   country = models.CharField(max_length=3)
   aproved = models.BooleanField(default=True)
   adminId = models.ForeignKey(Admin, on_delete=models.CASCADE, db_column="adminId")

   class Meta:
      db_table = 'app_admins_login'
      verbose_name = "admins login"
      verbose_name_plural = "admins login"
   
   def __str__(self):
      return self.ssid


class ContentMarks(models.Model):
   'Modelo de registro de marcadores de los adminitradores'
   nodeId = models.CharField(max_length=20, db_index=True)
   nodeType = models.CharField(max_length=20, choices=NodeTypes.choices)
   addedAt = models.DateTimeField(auto_now_add=True)
   adminId = models.ForeignKey(Admin, on_delete=models.CASCADE, db_column="adminId")

   class Meta:
      db_table = 'app_admins_content_mark'
      verbose_name = "admins mark"
      verbose_name_plural = "admins mark"
   
   def __str__(self):
      return f"{self.nodeType} - {self.nodeId}"