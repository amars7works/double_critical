"""
WSGI config for doublecritical project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from decouple import config
requires_system_checks = False


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        print("Set the %s environment variable" % (var_name))
        print("Current environment set to local")

'''
	This tells django which settings file to use, depending on 
	the value of the DJANGO_EXECUTION_ENVIRONMENT variable.
'''
DJANGO_EXECUTION_ENVIRONMENT = get_env_variable('DJANGO_EXECUTION_ENVIRONMENT')

if DJANGO_EXECUTION_ENVIRONMENT == 'STAGING':
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doublecritical.settings.staging")
elif DJANGO_EXECUTION_ENVIRONMENT == 'PRODUCTION':
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doublecritical.settings.production")
else:
	if not DJANGO_EXECUTION_ENVIRONMENT:
	  os.environ.setdefault("DJANGO_EXECUTION_ENVIRONMENT", 'LOCAL')
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", config('DJANGO_SETTINGS_MODULE', default=None))

application = get_wsgi_application()
