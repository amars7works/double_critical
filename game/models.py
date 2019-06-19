from django.db import models
from django.contrib.auth.models import User
from dc.models import FollowUser
from django.forms.models import model_to_dict



class GameCategory(models.Model):
	STATUS_CHOICES = (
		('review','REVIEW'),
		('published','PUBLISHED')
		)
	category_name = models.CharField(max_length=60)
	status = models.CharField(
				choices = STATUS_CHOICES,
				default='review',
				max_length = 10
				)

	def __str__(self):
		return self.category_name

	class Meta:
		unique_together = ('category_name',)

class Designer(models.Model):
	designer_name = models.CharField(max_length=60)

	def __str__(self):
		return self.designer_name

	class Meta:
		unique_together = ('designer_name',)

class Artist(models.Model):
	artist_name = models.CharField(max_length=60)

	def __str__(self):
		return self.artist_name

	class Meta:
		unique_together = ('artist_name',)

class Publisher(models.Model):
	publisher_name = models.CharField(max_length=60)

	def __str__(self):
		return self.publisher_name

	class Meta:
		unique_together = ('publisher_name',)

class Mechanism(models.Model):
	mechanism = models.CharField(max_length=60)

	def __str__(self):
		return self.mechanism

	class Meta:
		unique_together = ('mechanism',)

class Tags(models.Model):
	tag_name = models.CharField(max_length=30)

	def __str__(self):
		return self.tag_name

class GameGallery(models.Model):

	images = models.ImageField(upload_to='upload/',null=True)
	videos = models.FileField(upload_to='upload/',null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user

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

	category = models.ManyToManyField(GameCategory)

	year_published = models.IntegerField(null=True)
	minimum_players = models.IntegerField(null=True)
	maximum_players = models.IntegerField(null=True)
	mfg_suggested_ages = models.CharField(max_length=20, null=True)
	minimum_playing_time = models.CharField(max_length=20, null=True)
	maximum_playing_time = models.CharField(max_length=20, null=True)
	designer = models.ManyToManyField(Designer)
	artist = models.ManyToManyField(Artist)
	publisher = models.ManyToManyField(Publisher)
	mechanism = models.ManyToManyField(Mechanism)
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
	description = models.CharField(max_length=250,blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)
	data = models.CharField(null=True, blank=True,max_length=60)
	scan_type = models.CharField(null=True, blank=True,max_length=60)

	def __str__(self):
		return self.name

	class Meta:
		unique_together = ('name',)

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
		return self.game.name
	
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


class GameTag(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

	def __str__(self):
		return self.game.name

	class Meta:
		unique_together = ('game', 'tag')

class GameFeed(models.Model):
	object_type = models.CharField(max_length=30)
	object_id = models.IntegerField(blank=True,null=True)
	object_created_at = models.DateTimeField(auto_now_add=True, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.object_type

class LikeLog(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	object_id = models.IntegerField(blank=True,null=True)
	object_type = models.CharField(max_length=30)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.object_type

	class Meta:
		unique_together = ('object_type','object_id')


class SocialBase(models.Model):
	likes_count = models.IntegerField(blank=True,null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	object_type = models.CharField(max_length=30)

	def __str__(self):
		return self.object_type

class GameComment(SocialBase):
	comment = models.TextField(blank=True,null=True)
	users = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.comment

	class Meta:
		unique_together = ('users','game')


	def save(self, *args, **kwargs):
	    super(SocialBase, self).save(*args, **kwargs)
	    follow_users = FollowUser.objects.filter(follower = self.user)
	    game_feed_item = GameFeed(user=self.user,object_type='GameComment', 
	    				object_id = self.id,
	    				game = self.game,
	    				object_created_at=self.created_at)
	    
	    game_feed_item.save()
	    for follow_user in follow_users:
	    	game_feed = GameFeed(user=follow_user.follower,object_type='GameComment',
	    					object_id = self.id,
	    					game = self.game,
	    					object_created_at=self.created_at)
	    	game_feed.save()

