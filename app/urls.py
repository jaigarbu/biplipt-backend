from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from app.graphql.schema import Schema

urlpatterns = [
    path('data/api/', csrf_exempt(GraphQLView.as_view(graphiql=False, schema=Schema)))
]