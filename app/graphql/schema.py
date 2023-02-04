import graphene

from app.graphql.Mutation.genre import CreateGenre
from app.graphql.Mutation.user import CreateUser, DeleteUser, LoginUser
from app.graphql.Query.genre import GenreQuery
from app.graphql.Query.user import UserQuery


class Query(
   UserQuery,
   GenreQuery,
   graphene.ObjectType
):
   'Query principal de GraphQL API'
   pass


class Mutation(graphene.ObjectType):
   'Mutation principal de la API GraphQL'
   createGenre = CreateGenre.Field()
   
   createUser = CreateUser.Field()
   deleteUser = DeleteUser.Field()
   login = LoginUser.Field()


Schema = graphene.Schema(query=Query, mutation=Mutation)
