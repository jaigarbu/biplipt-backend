
def get_IP(request):
   'Obtiene la dirección IP del usuario'
   client_ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
   if client_ip is None:
      client_ip = request.META.get('HTTP_X_REAL_IP', None)
   if client_ip is None:
      client_ip = request.META.get('REMOTE_ADDR', None)
   return client_ip

