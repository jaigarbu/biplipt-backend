from django.db import models
from django.utils.translation import gettext as _


class VisibilityOptions(models.TextChoices):
   'Opciones de  visibilidad de contenido'
   Public = 'public', _('Público')
   Private = 'private', _('Privado, artista y adminitrador pueden interactuar')
   Restricted = 'restricted', _('Restringido, todos los  moderadores pueden interactuar')
   Block = 'block', _('Bloqueado, solo adminitrador puede interactuar')


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