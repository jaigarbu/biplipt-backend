from graphene_django import DjangoObjectType

from app.models.genres import Genre


class GenreType(DjangoObjectType):
	'Tipo de dato de los géneros'
	class Meta:
		model = Genre