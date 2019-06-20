from .base import *
from decouple import Csv, config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = 'staging'

ALLOWED_HOSTS =  ['*']

SECRET_KEY = '4rq1*w#u!4ew5f-d7+xa#x4ne12*clbw7921csz#0u8wa_yvm$'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'double_critical',
        'USER': 'double-critical',
        'PASSWORD': 'dc123456',
        'HOST': '127.0.0.1',
        'PORT': '5432',
     }
}

ROOT_URL = "https://dc.s7works.io/"

#config('ALLOWED_HOSTS', cast=Csv())
