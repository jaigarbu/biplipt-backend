import graphene


class OrderBy(graphene.Enum):
   ID_asc = "id_asc"
   ID_desc = "id_desc"
   name_asc = "name_asc"
   name_desc = "name_desc"
   addedAt_asc = "addedAt_asc"
   addedAt_desc = "addedAt_desc"
   updatedAt_asc = "updatedAt_asc"
   updatedAt_desc = "updatedAt_desc"


class GenreOrderBy(graphene.Enum):
   ID_asc = "id_asc"
   ID_desc = "id_desc"
   name_asc = "name_asc"
   name_desc = "name_desc"
   addedAt_asc = "addedAt_asc"
   addedAt_desc = "addedAt_desc"
   updatedAt_asc = "updatedAt_asc"
   updatedAt_desc = "updatedAt_desc"