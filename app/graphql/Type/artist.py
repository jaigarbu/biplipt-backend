from graphene_django import DjangoObjectType

from app.models.artists import Artist, ArtistImages


class ArtistType(DjangoObjectType):
   class Meta:
      model = Artist


class ArtistImagesType(DjangoObjectType):
   class Meta:
      model = ArtistImages
