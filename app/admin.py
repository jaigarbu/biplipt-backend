from django.contrib import admin

from app.models.admins import Admins, AdminsLogin, ContentMarks
from app.models.albums import AlbumFT, AlbumModified, Albums
from app.models.artists import ArtistImages, ArtistModified, Artists
from app.models.genres import GenreModified, Genres
from app.models.lyrics import (LyricFT, LyricLikes, LyricModified, Lyrics,
                               LyricVersions, LyricVersionsModified)
from app.models.temporals import TemporalLyrics, TemporalTranslate
from app.models.translates import Translates, TranslatesModified
from app.models.users import UserLogins, Users

# Register your models here.
admin.site.register([Admins, AdminsLogin, ContentMarks])
admin.site.register([Albums, AlbumFT, AlbumModified])
admin.site.register([Artists, ArtistModified, ArtistImages])
admin.site.register([Genres, GenreModified])
admin.site.register([Lyrics, LyricFT, LyricLikes, LyricModified, LyricVersionsModified, LyricVersions])
admin.site.register([TemporalLyrics, TemporalTranslate])
admin.site.register([Translates, TranslatesModified])
admin.site.register([Users, UserLogins])
