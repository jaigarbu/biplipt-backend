from graphene_django import DjangoObjectType

from app.models.lyric_versions import (LyricVersionLikes, LyricVersions,
                                       LyricVersionsModifications)
from app.models.lyrics import Lyric, LyricFT, LyricLikes, LyricModifications


class LyricType(DjangoObjectType):
   class Meta:
      model = Lyric


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
      model = LyricVersionLikes


class LyricModificationsType(DjangoObjectType):
   class Meta:
      model = LyricModifications


class LyricVersionModificationsType(DjangoObjectType):
   class Meta:
      model = LyricVersionsModifications