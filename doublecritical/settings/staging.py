from .base import *
from decouple import Csv, config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = 'staging'

ALLOWED_HOSTS =  ['*']

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'HELLO_DJANGO',
		'USER': 'U_HELLO',
		'PASSWORD': 'hA8(scA@!fg3*sc&xaGh&6%-l<._&xCf',
		'HOST': '127.0.0.1',
		'PORT': 5432 # default postgres port
	}
}

#config('ALLOWED_HOSTS', cast=Csv())
