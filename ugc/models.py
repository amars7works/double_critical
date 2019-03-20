from django.db import models
from django.contrib.auth.models import User
from game.models import Game


class UGC(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	ugc_title = models.CharField(max_length=30)
	like_count = models.IntegerField(blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.ugc_title

	class Meta:
		unique_together = ('user', 'game', 'ugc_title')

class UGCLike(models.Model):
	LIKE_CHOICES = (
		('+1', 'LIKE'),
		('-1', 'DISLIKE'),
		('0', 'NEUTRAL'))
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	ugc = models.ForeignKey(UGC, on_delete=models.CASCADE)
	like_type = models.CharField(max_length=10,choices=LIKE_CHOICES, default='0')
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.user.username

	class Meta:
		unique_together = ('user', 'ugc')

class UGCComment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	ugc_comment = models.TextField(blank=True,null=True)
	ugc = models.ForeignKey(UGC, on_delete=models.CASCADE)
	
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return self.ugc_comment

	class Meta:
		unique_together = ('user', 'game','ugc')

class UGCCommentLike(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	ugccomment = models.ForeignKey(UGCComment, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	ugc = models.ForeignKey(UGC, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

	class Meta:
		unique_together = ('user', 'ugccomment', 'game', 'ugc')

class UGCReport(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	ugc = models.ForeignKey(UGC, on_delete = models.CASCADE)
	created_at = models.DateTimeField(auto_now_add = True)
	description = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.user.username

	class Meta:
		unique_together = ('user', 'ugc')
