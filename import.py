import csv,sys,os
import django
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

# Export the settings before running this file
sys.path.append("/home/BGG/double-critical/")

os.environ['DJANGO_SETTINGS_MODULE'] = 'double_critical.settings.local'

django.setup()

data = csv.reader(open("data.csv", 'r'))
from registration.models import Country
for row in data:

	if row[0] != 'country_name':
		post = Country()
		post.country_name = row[0]
		post.country_code = row[1]
		try:
			country_obj = Country.objects.get(
					country_name=post.country_name,
					country_code=post.country_code)
		except ObjectDoesNotExist:
			post.save()