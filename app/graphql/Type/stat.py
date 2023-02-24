from graphene_django import DjangoObjectType

from app.models.stats import AlbumWeekRank, LyricWeekRank


class LyricWeekStatsType(DjangoObjectType):
   class Meta:
      model = LyricWeekRank


class AlbumWeekStatsType(DjangoObjectType):
   class Meta:
      model = AlbumWeekRank