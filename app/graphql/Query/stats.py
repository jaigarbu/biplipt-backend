import graphene
from django.utils.translation import gettext as _
from graphql import GraphQLError

from app.controllers.stats import StatsController
from app.graphql.Type.stat import AlbumWeekStatsType, LyricWeekStatsType


class StatsQuery(graphene.ObjectType):
   
   getWeekLyricTop = graphene.List(LyricWeekStatsType, limit=graphene.Int(required=False))
   getWeekAlbumTop = graphene.List(AlbumWeekStatsType, limit=graphene.Int(required=False))
   
   
   # resolvers
   def resolve_getWeekLyricTop(root, info, limit=10):
      try:
         data = StatsController.getWeekTopLyricStats(limit)
         return data
      except Exception as e:
         print(e.args)
         return GraphQLError(_('No podemos realizar la consunta, presentamos errores internos'))
   
   def resolve_getWeekAlbumTop(root, info, limit=6):
      data = StatsController.getWeekTopAlbumStats(limit)
      return data