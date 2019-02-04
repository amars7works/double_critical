import csv,sys,os
import django
from registration.models import Country


sys.path.append("/home/BGG/double-critical/")

os.environ['DJANGO_SETTINGS_MODULE'] = 'doublecritical.settings.local'

django.setup()


data = csv.reader(open("data.csv", 'r'))
for row in data:
	if row[0] != 'country_name':
		post = Country()
		post.country_name = row[0]
		post.country_code = row[1]
		post.save()