import datetime

from django.db.models import F

from app.models.albums import Album
from app.models.lyrics import Lyric
from app.models.stats import (AlbumChart, AlbumRank, AlbumWeekChart,
                              AlbumWeekRank, LyricChart, LyricRank,
                              LyricWeekChart, LyricWeekRank)


class StatsController:
   
   
   @classmethod
   def registerDate(cls, model: LyricChart|AlbumChart) -> LyricChart|AlbumChart:
      """Registra la fecha actual para iniciar estadisticas diarias
      
      :param `model: LyricChart | AlbumChart` — Modelo al que se le va a realizar el registro de estadisticas
      :return — LyricChart|AlbumChart
      """
      # determinar tiempo actual
      dateNow = datetime.datetime.now().strftime('%Y-%m-%d')
      
      try:
         # comprobar existencia de la fecha actual y en caso de no existir crear la entrada      
         chart = model.objects.get(date=dateNow)
         return chart
      except model.DoesNotExist:
         chart = model.objects.create(date=dateNow)
         return chart


   @classmethod
   def registerWeek(cls, model: LyricWeekChart|AlbumWeekChart) -> LyricWeekChart|AlbumWeekChart:
      """Registra la semana actual para iniciar estadisticas por semana
      
      :param `model: LyricWeekChart | AlbumWeekChart` — Modelo al que se le realiza el registro de estadisticas
      :return — LyricWeekChart|AlbumWeekChart
      """
      # determinar semana actual
      currentWeek = datetime.date.today().isocalendar()[1]
      
      try:
         # comprobar existencia de la semana actual y en caso de no existir crear la entrada 
         chart = model.objects.get(week=currentWeek)
         return chart
      except model.DoesNotExist:
         chart = model.objects.create(week=currentWeek)
         return chart

   
   @classmethod
   def setLyricStats(cls, lyric: Lyric) -> bool:
      """Inserta una visita en la base de datos de la letra pasada por parametro
      
      :param `lyric: Lyric` — Letra a la cual se le realiza el registro
      """
      # Comprobar existencia de fecha actual antes de realizar registro si no está disponible se crea
      chart = cls.registerDate(model=LyricChart)
      
      # Validar existencia de letra en el ranking diario si no está se inserta, si está se incrementa sus vistas
      rank = chart.lyrics.filter(id=lyric.id).exists()
      if not rank:
         chart.lyrics.add(lyric)
      else:
         LyricRank.objects.filter(lyric_id=lyric.id, chart_id=chart.id).update(views=F('views') + 1)
      return True


   @classmethod
   def setWeekLyricStats(cls, lyric: Lyric) -> bool:
      """Registra una visita en la semana actual de la letra pasada por parámetro
      
      :param `lyric: Lyric` — Letra relacionada a la que se le realizará el registro
      """      
      # Comprobar existencia de semana en base de datos
      weekChart = cls.registerWeek(model=LyricWeekChart)
      
      # Validar existencia de letra en la semana actual. Si está disponible se incrementa sus visitas si no se
      # crea el registro correspondiente
      weekRank = weekChart.lyrics.filter(id=lyric.id).exists()
      if weekRank:
         LyricWeekRank.objects.filter(lyric_id=lyric.id, chart_id=weekChart.id).update(views=F('views') + 1)
      else:
         weekChart.lyrics.add(lyric)
      return True


   @classmethod
   def getWeekTopLyricStats(cls, limit: int=10):
      """Obtiene el ranking semanal de las letras mas visitadas
      
      :param `limit: int` — Limite de resultados que serán consultados, Default `10`
      :return — LyricWeekRank
      """      
      # Determinar la semana actual en la base de datos. En caso de no existir esta es creada
      currentWeek = cls.registerWeek(model=LyricWeekChart)
      
      # Consultar ranking de letras relacionadas
      lyrics = LyricWeekRank.objects.filter(chart_id=currentWeek.id).order_by('-views')[0:limit]
      return lyrics


   @classmethod
   def setAlbumStats(cls, album: Album) -> bool:
      """Registra una visita del álbum pasado por parametro en la fecha actual
      
      :param `album: Album` — Album a realizar ranking
      :return — bool
      """      
      # Comprobar existencia de fecha actual antes de realizar registro si no está disponible se crea
      chart = cls.registerDate(model=AlbumChart)
      
      # Validar existencia de letra en el ranking diario si no está se inserta, si está se incrementa sus vistas
      rank = chart.albums.filter(id=album.id).exists()
      if not rank:
         chart.albums.add(album)
      else:
         AlbumRank.objects.filter(lyric_id=album.id, chart_id=chart.id).update(views=F('views') + 1)
      return True


   @classmethod
   def setWeekAlbumStats(cls, album: Album) -> bool:
      """Registra una visista al album pasado por parametro en la semana actual
      
      :param `album: Album` — Album a realizar ranking
      :return — bool
      """
      # Comprobar existencia de semana en base de datos
      weekChart = cls.registerWeek(model=AlbumWeekChart)
      
      # Validar existencia de letra en la semana actual. Si está disponible se incrementa sus visitas si no se
      # crea el registro correspondiente
      weekRank = weekChart.albums.filter(id=album.id).exists()
      if weekRank:
         AlbumWeekChart.objects.filter(lyric_id=album.id, chart_id=weekChart.id).update(views=F('views') + 1)
      else:
         weekChart.albums.add(album)
      return True


   @classmethod
   def getWeekTopAlbumStats(cls, limit: int=6):
      """Obtiene el top de los álbumes más visitados de la semana
      
      :param `limit: int` — Limite de resultados a mostrar. Default `6`
      :return — _type_
      """
      # Determinar la semana actual en la base de datos. En caso de no existir esta es creada
      currentWeek = cls.registerWeek(model=AlbumWeekChart)
      
      # Consultar ranking de letras relacionadas
      albums = AlbumWeekRank.objects.filter(chart_id=currentWeek.id).order_by('-views')[0:limit]
      return albums

