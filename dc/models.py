from django.db import models
from django.contrib.auth.models import User

class FollowUser(models.Model):
	follower = models.ForeignKey(User, null=True, related_name='follower')
	following = models.ForeignKey(User, null=True, related_name='following')
	follow_count = models.IntegerField(blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.follower.username

	def get_follower(self):
		return self.following.username

	def get_following(self):
		return self.follower.username

	class Meta:
		unique_together = ('follower', 'following')
