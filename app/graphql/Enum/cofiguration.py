import graphene


class UserStatusEnum(graphene.Enum):
   Active = 'active'
   Unverified = 'unverified'
   Suspended = 'suspended'
   Restricted = 'restricted'
   Block = 'block'


class AdminStatusEnum(graphene.Enum):
   Artist = '2'
   Moderator = '3'


class ItemVisibilityEnum(graphene.Enum):
   Public = 'public'
   Private = 'private'
   Restricted = 'restricted'
   Block = 'block'


class ArtistTypeEnum(graphene.Enum):
   Band = 'band'
   Chorister = 'choir'
   Composer = 'composer'
   Dj = 'DJ'
   Group = 'group'
   Instrumentalist = 'instrumentalist'
   Musician = 'musician'
   Orchestra = 'orchestra'
   Other = 'other'
   Producer = 'producer'
   Rapper = 'rapper'
   Singer = 'singer'
   

class AlbumTypeEnum(graphene.Enum):
   Album = 'album'
   Single = 'single'