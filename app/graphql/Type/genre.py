import graphene
from graphene_django import DjangoObjectType

from app.models.genres import Genres


class GenreType(DjangoObjectType):
	'Tipo de dato de los géneros'
	class Meta:
		model = Genres


class GenreData(graphene.ObjectType):
	'Tipo de dato para la respuesta de los géneros'
	data = graphene.Field(GenreType)
	lyricsCount = graphene.Int()
	albumsCount = graphene.Int()
	
	# resolvers
	def resolve_lyricsCount(root, info):
		print(root)
		print(info)
		return 10