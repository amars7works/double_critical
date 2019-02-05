from django.db import models
from django.contrib.auth.models import User


class GameExtend(models.Model):
	expansion =models.TextField(max_length=60, null=True)
	expands = models.TextField(null=True)
	integrates_with = models.TextField(null=True)
	contains = models.TextField(null=True)
	contained_in = models.TextField(null=True)
	reimplemented_by = models.TextField(null=True)
	reimplements = models.TextField(null=True)
	family = models.TextField(null=True)
	video_game_adaptation = models.TextField(null=True)

	def __str__(self):
		return self.expansion


class Game(models.Model):

	STATUS_CHOICES = (
		('review','REVIEW'),
		('published','PUBLISHED')
		)
	HOTORNOT_CHOICES = (
		(True,'TRUE'),
		(False,'FALSE')
		)
	ORIGIN_CHOICES = (
		('publisher', 'PUBLISHER'),
		('self published', 'SELF PUBLISHED'),
		('kickstarted','KICKSTARTED')
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
	note_to_admin = models.TextField(null=True)
	
	extend = models.ForeignKey(
				GameExtend, 
				on_delete=models.CASCADE,
				related_name='extend')
	status = models.CharField(
				choices = STATUS_CHOICES,
				default='review',
				max_length = 10
				)
	hotornot = models.BooleanField(default=False, choices = HOTORNOT_CHOICES)
	upc = models.CharField(max_length=20)
	origin = models.CharField(
				choices=ORIGIN_CHOICES,
				default='publisher',
				max_length=10
				)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return self.name


class GameFollow(models.Model):
	FOLLOW = (
		(True,'TRUE'),
		(False,'FALSE')
		)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	follow_game = models.BooleanField(
				choices=FOLLOW,
				default=False
				)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return self.user.username


class GameComment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	game_comments = models.TextField(blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return self.user.username


class RateGame(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	game_rating = models.IntegerField(null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return self.user.username


class Collection(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return self.user.username


class UGCComment(models.Model):
	LIKE = (
		(True,'TRUE'),
		(False,'FALSE')
		)

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	ugc_comments = models.TextField(blank=True,null=True)
	comments_like = models.BooleanField(
				choices=LIKE,
				default=False
				)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return self.user.username


class UGC(models.Model):
	LIKE = (
		(True,'TRUE'),
		(False,'FALSE')
		)

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	ugc_title = models.CharField(max_length=30)
	like = models.BooleanField(
				choices=LIKE,
				default=False
				)
	comments = models.ForeignKey(UGCComment, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return self.user.username
