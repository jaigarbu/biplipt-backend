from django.contrib import admin

from app.models.admins import Admin, AdminsLogin, ContentMarks
from app.models.albums import Album, AlbumFT, AlbumModifications
from app.models.artists import Artist, ArtistImages, ArtistModifications
from app.models.genres import Genre, GenreModifications
from app.models.lyric_versions import (LyricVersionLikes, LyricVersions,
                                       LyricVersionsModifications)
from app.models.lyrics import Lyric, LyricFT, LyricLikes, LyricModifications
from app.models.stats import (AlbumChart, AlbumRank, AlbumWeekChart,
                              AlbumWeekRank, LyricChart, LyricRank,
                              LyricWeekChart, LyricWeekRank)
from app.models.temporals import TemporalLyric, TemporalTranslate
from app.models.translates import Translate, TranslateModifications
from app.models.users import User, UsersLogin

# Register your models here.
admin.site.register([Admin, AdminsLogin, ContentMarks])
admin.site.register([Album, AlbumFT, AlbumModifications])
admin.site.register([Artist, ArtistModifications, ArtistImages])
admin.site.register([GenreModifications, Genre])
admin.site.register([Lyric, LyricFT, LyricLikes, LyricModifications])
admin.site.register([LyricVersions, LyricVersionsModifications, LyricVersionLikes])
admin.site.register([TemporalLyric, TemporalTranslate])
admin.site.register([Translate, TranslateModifications])
admin.site.register([User, UsersLogin])

# modelos de estadísticas
admin.site.register([LyricChart, LyricRank, LyricWeekChart, LyricWeekRank])
admin.site.register([AlbumChart, AlbumWeekChart, AlbumRank, AlbumWeekRank])