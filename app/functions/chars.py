import random
import re


def random_chars(length: int = 1) -> str:
   """Genera carácteres alfanuméricos aleatorios
   
   :param `length: int` — Cantidad de caracteres a generar. Default `1`
   :return — str
   """  
   ouput = ""
   chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
   for i in range(length):
      ouput += random.choice(chars)
   return ouput


def random_numbers(length: int = 1) -> str:
   """Genera carácteres numéricos aleatoreos
   
   :param `length: int` — Cantidad de caracteres a generar. Default `1`
   :return — str
   """  
   ouput = ""
   chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
   for i in range(length):
      ouput += random.choice(chars)
   return ouput


def normalize_string(value: str, type: str = None) -> str:
   """Normaliza un string
   
   :param `value: str` — Valor a normalizar
   :param `type: str` — Tipo de normalización `text`, `url`, `name`. Default `None`
   :return — str
   """  
   translator = str.maketrans('ÃÀÁÄÂÈÉËÊÌÍÏÎÒÓÖÔÙÚÜÛãàáäâèéëêìíïîòóöôùúüûÑñÇç', 'AAAAAEEEEIIIIOOOOUUUUaaaaaeeeeiiiioooouuuuNnCc')
   ouput = str.strip(value)
   
   # comílar expresiones
   expText = re.compile(r'[^a-z0-9\s]', re.IGNORECASE)
   expName = re.compile(r'[^a-zA-ZÀ-ÿ\u00f1\u00d1\s]', re.IGNORECASE)
   
   if type == 'text':
      ouput = ouput.translate(translator)
      ouput = re.sub(r'\s{2,}', ' ', ouput)
   elif type == 'url':
      ouput = ouput.translate(translator)
      ouput = str.lower(ouput)
      ouput = re.sub(r'[^a-z0-9]', ' ', ouput)
      ouput = str.strip(value).lower()
      ouput = re.sub(r'\s{1,}', '-', ouput)
   elif type == 'title':
      ouput = re.sub(expName, '', ouput)
      ouput = re.sub(r'\s{2,}', ' ', ouput)
      ouput = str.title(ouput)
   else:
      ouput = re.sub(expText, '', ouput)
      ouput = re.sub(r'\s{2,}', ' ', ouput)
   return ouput