#!/usr/bin/env python
import os
import sys

from decouple import config

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        print("Set the %s environment variable" % (var_name))
        print("Current environment set to local")


if __name__ == "__main__":
  '''
    This tells django which settings file to use, depending on 
    the value of the DJANGO_EXECUTION_ENVIRONMENT variable.
  '''
  DJANGO_EXECUTION_ENVIRONMENT = get_env_variable('DJANGO_EXECUTION_ENVIRONMENT')
  if DJANGO_EXECUTION_ENVIRONMENT == 'STAGING':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "double_critical.settings.staging")
  elif DJANGO_EXECUTION_ENVIRONMENT == 'PRODUCTION':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "double_critical.settings.production")
  else:
    if not DJANGO_EXECUTION_ENVIRONMENT:
      os.environ.setdefault("DJANGO_EXECUTION_ENVIRONMENT", 'LOCAL')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", config('DJANGO_SETTINGS_MODULE', default=None))

  from django.core.management import execute_from_command_line
  execute_from_command_line(sys.argv)