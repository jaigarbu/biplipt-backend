from graphene_django import DjangoObjectType

from app.models.lyrics import (LyricFT, LyricLikes, LyricModified, Lyrics,
                               LyricVersions, LyricVersionsLikes,
                               LyricVersionsModified)


class LyricType(DjangoObjectType):
   class Meta:
      model = Lyrics


class LyricVersionType(DjangoObjectType):
   class Meta:
      model = LyricVersions


class LyricFeaturingType(DjangoObjectType):
   class Meta:
      model = LyricFT


class LyricLikesType(DjangoObjectType):
   class Meta:
      model = LyricLikes


class LyricVersionLikesType(DjangoObjectType):
   class Meta:
      model = LyricVersionsLikes


class LyricModifiedType(DjangoObjectType):
   class Meta:
      model = LyricModified


class LyricVersionModifiedType(DjangoObjectType):
   class Meta:
      model = LyricVersionsModified