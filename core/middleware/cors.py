from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin


class CorsMiddleware(MiddlewareMixin):
   def __call__(self, request: HttpRequest, response: HttpResponse):
      response['Access-Control-Allow-Origin'] = '*'
      response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
      response['Access-Control-Allow-Headers'] = 'Origin, Content-Type'
      return response
