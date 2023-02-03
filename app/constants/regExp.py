# Expresiones regulares universales y de sistema
EXP_IP = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
EXP_URL = r'^https?:\/\/[\w\-]+(\.[\w\-]+)+[\/#?]?.*$'
EXP_LOCALE = r'^[a-z]{2}\-[a-z]{2}$'


# Expresiones generales validas para -> ES, FR, EN, PT, IT
EXP_CELLPHONE = r'^[0-9]{10}$'
EXP_EMAIL = r'^[a-z0-9_-]+(?:\.[a-z0-9_-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$'
EXP_GENDER = r'^(M|F|O)$'
EXP_PASSWORD = r'^[\w\d\W]{8,32}$'
EXP_USERNAME = r'^[a-z0-9]+([a-z0-9-_\.][a-z0-9])+$'

EXP_ALBUM_NAME = r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s[a-zA-ZÀ-ÿ\u00f1\u00d1\-\:]+)*$'
EXP_GENRE_NAME = r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s[a-zA-ZÀ-ÿ\u00f1\u00d1\-]+)*$'
EXP_LANG = r'^[a-z]{2}$'
EXP_LANGUAGE = r'[^=.\-/\\\>\<$#%&!"?\'()]+'
EXP_NAME = r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s[a-zA-ZÀ-ÿ\u00f1\u00d1]+)*$'
EXP_NATIVE_NAME = r'[=.\-/\\\>\<$#%&!"?\'()]+'

EXP_DATE = r'^\w{4}(\-\w{2}){2}$'
EXP_ORDERBY_GLOBAL = r'^(id|name|added|updated)\_(asc|desc)$'
EXP_TOKEN_URL = r'^[a-z]+(\-[a-z]+)*$'
EXP_DNS = r'^[a-z0-9=#+]+$'

EXP_ARTIST_TYPE = r'^[a-z]+(\s[a-z]+){0,3}$'
EXP_COUNTRY_CODE = r'^[A-Z]{2,3}$'
EXP_COUNTRY_NAME = r'^[a-z]+(\s[a-z\'-]+)*$'


# Expresiones validas para -> Japonés JA
EXP_JA_NAME = r'^[\u4E00-\u9FAF\u3040-\u309F\u30A0-\u30FF]+$'
# /^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$/g
# ^[\u4E00-\u9FAF\u3040-\u309F\u30A0-\u30FF]+$
