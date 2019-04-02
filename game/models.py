from django.db import models
from django.contrib.auth.models import User

class GameCategory(models.Model):
	category_name = models.CharField(max_length=60, primary_key=True)

	def __str__(self):
		return self.category_name

class Tags(models.Model):
	tag_name = models.CharField(max_length=30, primary_key=True)

	def __str__(self):
		return self.tag_name

class Game(models.Model):

	STATUS_CHOICES = (
		('review','REVIEW'),
		('published','PUBLISHED')
		)
	ORIGIN_CHOICES = (
		('publisher', 'PUBLISHER'),
		('self published', 'SELF PUBLISHED'),
		('kickstarted','KICKSTARTED')
		)

	name = models.CharField(max_length=80, null=True)

	category = models.ForeignKey(GameCategory, on_delete=models.CASCADE,null=True)
	tag = models.ForeignKey(Tags, on_delete=models.CASCADE, null=True)

	year_published = models.IntegerField(null=True)
	minimum_players = models.IntegerField(null=True)
	maximum_players = models.IntegerField(null=True)
	mfg_suggested_ages = models.CharField(max_length=20, null=True)
	minimum_playing_time = models.CharField(max_length=20, null=True)
	maximum_playing_time = models.CharField(max_length=20, null=True)
	designer = models.CharField(max_length=40, null=True)
	artist = models.CharField(max_length=40, null=True)
	publisher = models.CharField(max_length=60, null=True)
	mechanism = models.CharField(max_length=60, null=True)
	views = models.IntegerField(default=0,blank=True,null=True)
	like_count = models.IntegerField(default=0,blank=True,null=True)
	dislike_count = models.IntegerField(default=0,blank=True,null=True)
	game_status = models.CharField(
				choices = STATUS_CHOICES,
				default='review',
				max_length = 10
				)
	hotornot = models.BooleanField(default=False)
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

	class Meta:
		unique_together = ('name', 'category')

class GameExtend(models.Model):
	game = models.OneToOneField(Game, on_delete=models.CASCADE,null=True)
	expansion =models.CharField(max_length=80, null=True)
	expands = models.CharField(max_length=80, null=True)
	integrates_with = models.CharField(max_length=80, null=True)
	contains = models.CharField(max_length=80, null=True)
	contained_in = models.CharField(max_length=80, null=True)
	reimplemented_by = models.CharField(max_length=80, null=True)
	reimplements = models.CharField(max_length=80, null=True)
	family = models.CharField(max_length=80, null=True)
	video_game_adaptation = models.CharField(max_length=80, null=True)
	note_to_admin = models.CharField(max_length=80, null=True)

	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return self.expansion
	
	class Meta:
		unique_together = ('game',)

class FollowGame(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.game.name

	class Meta:
		unique_together = ('user', 'game')

class RateGame(models.Model):
	GAME_RATING = (
		('love','LOVE'),
		('like','LIKE'),
		('dislike','DISLIKE'),
		('hate','HATE')
		)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	game_rating = models.CharField(
				max_length=10,
				choices=GAME_RATING,
				default=None
				)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.user.username

	class Meta:
		unique_together = ('user', 'game')

class GameCollection(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.game.name

	class Meta:
		unique_together = ('user', 'game')

class LikeGame(models.Model):
	GAME_LIKE = (
		('like','LIKE'),
		('dislike','DISLIKE')
		)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	views = models.IntegerField(blank=True,null=True, default=0)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	game_like = models.CharField(
				max_length=10,
				choices=GAME_LIKE,
				default=None
				)

	def __str__(self):
		return self.game.name

	class Meta:
		unique_together = ('user', 'game')


# class GameTag(models.Model):
# 	game_name = models.ForeignKey(Game, on_delete=models.CASCADE, 
# 							related_name='game_name')
# 	tag_name = models.ForeignKey(Tags, on_delete=models.CASCADE)

# 	def __str__(self):
# 		return self.game_name.name

# 	class Meta:
# 		unique_together = ('game_name', 'tag_name')
