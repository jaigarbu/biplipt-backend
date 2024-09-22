import graphene

from app.graphql.Mutation.admin import CreateAdmin
from app.graphql.Mutation.album import CreateAlbum
from app.graphql.Mutation.artist import CreateArtist, UpdateArtist
from app.graphql.Mutation.genre import CreateGenre, DeleteGenre, UpdateGenre
from app.graphql.Mutation.user import CreateUser, DeleteUser, LoginUser
from app.graphql.Query.album import AlbumQuery
from app.graphql.Query.artist import ArtistQuery
from app.graphql.Query.genre import GenreQuery
from app.graphql.Query.lyric import LyricQuery
from app.graphql.Query.stats import StatsQuery
from app.graphql.Query.system import SystemQuery
from app.graphql.Query.user import UserQuery


class Query(
   SystemQuery,
   UserQuery,
   GenreQuery,
   StatsQuery,
   LyricQuery,
   ArtistQuery,
   AlbumQuery,
   graphene.ObjectType
):
   'Query principal de GraphQL API'
   pass


class Mutation(graphene.ObjectType):
   'Mutation principal de la API GraphQL'
   createAdmin = CreateAdmin.Field()
   
   createArtist = CreateArtist.Field()
   updateArtist = UpdateArtist.Field()
   
   createAlbum = CreateAlbum.Field()
   
   createGenre = CreateGenre.Field()
   deleteGenre = DeleteGenre.Field()
   updateGenre = UpdateGenre.Field()
   
   createUser = CreateUser.Field()
   deleteUser = DeleteUser.Field()
   login = LoginUser.Field()


Schema = graphene.Schema(query=Query, mutation=Mutation)
