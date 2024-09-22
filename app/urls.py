from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_file_upload.django import FileUploadGraphQLView

from app.graphql.schema import Schema

from .views import getAlbumCover

urlpatterns = [
   path('data/api/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=False, schema=Schema))),
   path('storage/api/resource/<str:csrf>/data/<str:hash>', getAlbumCover)
]