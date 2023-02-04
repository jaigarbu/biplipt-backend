class HttpError(Exception):
   def __init__(self, message: str, code: int):
      self.message = message
      self.code = code


class HttpError404(Exception):
   def __init__(self, message: str, code = 404):
      self.message = message
      self.code = code


class HttpError400(Exception):
   def __init__(self, message: str, code = 400):
      self.message = message
      self.code = code


class HttpError500(Exception):
   def __init__(self, message: str, code = 500):
      self.message = message
      self.code = code


class ValidationError(Exception):
   def __init__(self, message: str, field = None, type = None):
      """Error de validacion

      :param `message: str` — Mensaje del error
      :param `field: str` — Campo donde ocurrio el error. Default `None`
      :param `type: str` — Tipo de error. Default `None`
      """      
      self.message = message
      self.field = field
      self.type = type
  