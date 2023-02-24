from django.db import models

from app.models.albums import Album
from app.models.lyrics import Lyric


# Estadisticas de letras
class LyricChart(models.Model):
   'Modelo de resgistro de estadisticas diarias para las letras'  
   date = models.DateField()
   lyrics = models.ManyToManyField(Lyric, related_name="+", through="LyricRank")
   
   class Meta:
      db_table = 'lyric_chart'
      verbose_name = 'lyric chart'
      verbose_name_plural ='lyric charts'
   
   def __str__(self):
      return self.date.strftime('%d-%m-%Y')


class LyricWeekChart(models.Model):
   'Modelo del registro de estadisdisticas semanales de las letras'
   week = models.PositiveSmallIntegerField()
   lyrics = models.ManyToManyField(Lyric, related_name="+", through="LyricWeekRank")

   class Meta:
      db_table = 'lyric_week_chart'
      verbose_name = 'lyric week charts'
      verbose_name_plural ='lyric week charts'

   def __str__(self):
      return str(self.week)


class LyricRank(models.Model):
   'Modelo de registro de visitas individuales de letras por dias'
   lyric = models.ForeignKey(Lyric, on_delete=models.CASCADE, related_name="+")
   chart = models.ForeignKey(LyricChart, on_delete=models.CASCADE)
   views = models.PositiveIntegerField(default=1)
   
   class Meta:
      db_table = 'lyric_rank'
      verbose_name = 'lyric rank'
      verbose_name_plural ='lyric ranks'
   
   def __str__(self):
      return str(self.views)


class LyricWeekRank(models.Model):
   'Modelo de registro de visitas individuales de letras por semana'
   lyric = models.ForeignKey(Lyric, on_delete=models.CASCADE, related_name="+")
   chart = models.ForeignKey(LyricWeekChart, on_delete=models.CASCADE)
   views = models.PositiveIntegerField(default=1)
   
   class Meta:
      db_table = 'lyric_week_rank'
      verbose_name = 'lyric week rank'
      verbose_name_plural ='lyric week ranks'
   
   def __str__(self):
      return str(self.lyric)


# Estadisticas de albumes
class AlbumChart(models.Model):
   'Modelo de resgistro de estadisticas diarias para los álbumes'  
   date = models.DateField()
   albums = models.ManyToManyField(Album, related_name="+", through="AlbumRank")
   
   class Meta:
      db_table = 'album_chart'
      verbose_name = 'album chart'
      verbose_name_plural ='album charts'
   
   def __str__(self):
      return self.date.strftime('%d-%m-%Y')


class AlbumWeekChart(models.Model):
   'Modelo de resgistro de estadisticas semanales de los álbumes'
   week = models.PositiveSmallIntegerField()
   albums = models.ManyToManyField(Album, related_name="+", through="AlbumWeekRank")

   class Meta:
      db_table = 'album_week_chart'
      verbose_name = 'album week charts'
      verbose_name_plural ='album week charts'

   def __str__(self):
      return str(self.week)


class AlbumRank(models.Model):
   'Modelo de registro de visitas individuales de los álbumes por dias'
   album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="+")
   chart = models.ForeignKey(AlbumChart, on_delete=models.CASCADE)
   views = models.PositiveIntegerField(default=1)
   
   class Meta:
      db_table = 'album_rank'
      verbose_name = 'album rank'
      verbose_name_plural ='album ranks'
   
   def __str__(self):
      return str(self.views)


class AlbumWeekRank(models.Model):
   'Modelo de registro de visitas individuales de los álbumes por semana'
   album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="+")
   chart = models.ForeignKey(AlbumWeekChart, on_delete=models.CASCADE)
   views = models.PositiveIntegerField(default=1)
   
   class Meta:
      db_table = 'album_week_rank'
      verbose_name = 'album week rank'
      verbose_name_plural ='album week ranks'
   
   def __str__(self):
      return str(self.album)