from django.db import models


class Game(models.Model):

	STATUS_CHOICES = (
		('review','REVIEW'),
		('published','PUBLISHED')
		)
	HOTORNOT_CHOICES = (
		(True,'TRUE'),
		(False,'FALSE')
		)

	name = models.CharField(max_length=20, null=True)
	year_published = models.IntegerField(null=True)
	minimum_players = models.IntegerField(null=True)
	maximum_players = models.IntegerField(null=True)
	mfg_suggested_ages = models.CharField(max_length=20, null=True)
	minimum_playing_time = models.CharField(max_length=20, null=True)
	maximum_playing_time = models.CharField(max_length=20, null=True)
	designer = models.CharField(max_length=40, null=True)
	artist = models.CharField(max_length=40, null=True)
	publisher = models.TextField(max_length=60, null=True)
	category = models.CharField(max_length=60, null=True)
	mechanism = models.CharField(max_length=60, null=True)
	expansion =models.TextField(max_length=60, null=True)
	expands = models.TextField(null=True)
	integrates_with = models.TextField(null=True)
	contains = models.TextField(null=True)
	contained_in = models.TextField(null=True)
	reimplemented_by = models.TextField(null=True)
	reimplements = models.TextField(null=True)
	family = models.TextField(null=True)
	video_game_adaptation = models.TextField(null=True)
	note_to_admin = models.TextField(null=True)
	
	status = models.CharField(
		choices = STATUS_CHOICES,
		default='review',
		max_length = 10
		)
	hotornot = models.BooleanField(default=False, choices = HOTORNOT_CHOICES)

	def __str__(self):
		return self.name