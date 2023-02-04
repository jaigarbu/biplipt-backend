import codecs
import time
from datetime import datetime

from authlib.jose import JsonWebKey, JsonWebToken


class TokenController:
   
   @classmethod
   def createJWK(cls, alg: str = 'oct', size: int = 512, crypt: bool = False) -> str:
      """Crea una clave para JWT

      :param `alg: str` — Algoritmo que se usará para crear la JWK. Default `'oct'`
      :param `size: int` — Longitud en bites de la JWK. Default `512`
      :param `crypt: bool` — Deternima se la JWK será para firmar o encriptar un token. Default `False`
      :return — string
      """
      key = JsonWebKey.generate_key(kty=alg, crv_or_size=size, is_private=True)
      if not crypt:
         return codecs.decode(key.get_op_key('sign'))
      else:
         return key.as_json()


   @classmethod
   def singToken(cls, payload: dict, key: str, expiration: int = 3600, crypt: bool = False) -> str:
      """Crea un JWT usando JWS
      
      :param `payload: dict` — Datos del payload
      :param `key: str` — Clave usada para firmar el token
      :param `expiration: int` — Tiempo de expiración del token en ms. Default `3600`
      :param `crypt: bool` — Determina si el JWT será encriptado o no. Default `False`
      :return — String
      """
      ms = datetime.now()
      claims = {
         'aud': 'biplipt.com',
         'exp': time.mktime(ms.timetuple()) + expiration,
         'iat': time.mktime(ms.timetuple()),
         # 'jti': HttpRequest.session.get('ssid'),
         'nbf': time.mktime(ms.timetuple()),
         'data': payload
      }
      headers = {'alg': 'HS512'}
      
      # construccion y firma del JWST
      jwt = JsonWebToken(['HS512'])
      jwtoken = jwt.encode(header=headers, payload=claims, key=key)
      return codecs.decode(jwtoken)
   
   
   @classmethod
   def verifyJWSToken(cls, key: str, token: str|None) -> dict|bool:
      """Verifica la validez de un JWT

      :param `key: str` — Clave usada para firmar el token
      :param `token: str | None` — String con el token a verificar
      :return — dict | bool
      """
      if not token:
         return False
      
      jwt = JsonWebToken(['HS512'])
      try:
         claims = jwt.decode(s=token, key=key)
         return claims.get('data')
      except Exception:
         return False