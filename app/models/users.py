from datetime import datetime

from django.db import models

from app.models.system import AccountStatus, GenderOptions


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
   
   class Meta:
      verbose_name = "user"
      verbose_name_plural = "users"


class UserLogins(models.Model):
   'Modelo de sessiones autorizadas'
   ssid = models.CharField(max_length=255)
   userAgent = models.CharField(max_length=300)
   loginAt = models.DateTimeField(default=datetime.now())
   ip = models.CharField(max_length=16)
   country = models.CharField(max_length=3)
   aproved = models.BooleanField(default=True)
   user = models.ForeignKey(Users, on_delete=models.CASCADE)
   
   class Meta:
      db_table = 'app_user_logins'
      verbose_name = "user login"
      verbose_name_plural = "user logins"
