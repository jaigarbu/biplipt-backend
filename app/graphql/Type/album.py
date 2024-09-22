from graphene_django import DjangoObjectType

from app.models.albums import Album, AlbumFT, AlbumModifications


class AlbumType(DjangoObjectType):
   class Meta:
      model = Album


class AlbumFeaturingType(DjangoObjectType):
   class Meta:
      model = AlbumFT


class AlbumModificationsType(DjangoObjectType):
   class Meta:
      model = AlbumModifications