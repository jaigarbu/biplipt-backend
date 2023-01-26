from datetime import datetime
from django.db import models
from django.utils.translation import gettext as _

class AccountStatus(models.TextChoices):
   'Opciones para los estados de las cuentas de usuario'
   Active = 'active', _('Cuenta activa')
   Unverified = 'unverified', _('Cuenta no verificada')
   Suspended = 'suspended', _('Cuenta suspendida')
   Restricted = 'restricted', _('Cuenta restringida')
   Block = 'block', _('Cuenta bloqueada')

class GenderOptions(models.TextChoices):
   'Opciones para el genero de los usuarios'
   Male = 'M', _('Masculino')
   Female = 'F', _('Femenino')
   Other = 'O', _('Otro')


class Users(models.Model):
   'Modelo de Usuario'
   id = models.BigAutoField(primary_key=True)
   status = models.CharField(max_length=11, choices=AccountStatus.choices, default=AccountStatus.Unverified)
   name = models.CharField(max_length=20)
   lastName = models.CharField(max_length=40)
   birthdate = models.DateField()
   country = models.CharField(max_length=2)
   gender = models.CharField(max_length=6, choices=GenderOptions.choices)
   language = models.CharField(max_length=20)
   username = models.CharField(max_length=20, unique=True)
   email = models.CharField(max_length=50, unique=True)
   password = models.CharField(max_length=255)
   photo = models.CharField(max_length=80, null=True)
   lastSeen = models.DateTimeField(null=True)
   activationKey = models.CharField(max_length=400, null=True)
   registeredAt = models.DateTimeField(default=datetime.now())
   updatedAt = models.DateTimeField(null=True)
   ip = models.CharField(max_length=16)


class UserLogins(models.Model):
   'Modelo de sessiones autorizadas'
   ssid = models.CharField(max_length=255)
   userAgent = models.CharField(max_length=300)
   loginAt = models.DateTimeField(default=datetime.now())
   ip = models.CharField(max_length=16)
   country = models.CharField(max_length=3)
   aproved = models.BooleanField(default=True)
   user = models.ForeignKey(Users, on_delete=models.CASCADE, name='userId')
