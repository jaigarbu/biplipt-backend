from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, render

from core.settings import BASE_DIR

# Create your views here.

def getAlbumCover(request, csrf: str, hash: str):
   archivo = open(BASE_DIR / f'storage/albums/{hash}', 'rb')
   response = FileResponse(archivo, as_attachment=False)
   # response['Content-Disposition'] = 'attachment; filename="{}"'.format(archivo.name)
   return response
