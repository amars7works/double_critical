from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4rq1*w#u!4ew5f-d7+xa#x4ne12*clbw7921csz#0u8wa_yvm$'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': base_dir_join('db.sqlite3'),
   }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'double_critical',
#         'USER': 'double-critical',
#         'PASSWORD': 'dc123456',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }
