from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.
class Article(models.Model):
	def_ups = {'upvoters': []}
	j_ups = json.dumps(def_ups)
	title = models.CharField(max_length=80)
	body = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField()
	author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
	media = models.ImageField(default='default.jpg', blank=True)
	upvotes = models.TextField(default=j_ups)

	def __str__(self):
		return self.title

	def preview(self):
		maxchar = 350
		return self.body[:maxchar] + "..." if len(self.body) > maxchar else self.body

	def remove_from_upvotes(self, username):
		ups = json.loads(self.upvotes)
		L = ups["upvoters"]
		L.remove(username)
		ups["upvoters"] = L
		self.upvotes = json.dumps(ups)

	def add_to_upvotes(self, username):
		ups = json.loads(self.upvotes)
		ups["upvoters"] += [username]
		self.upvotes = json.dumps(ups)

	def check_for_user(self, username):
		ups = json.loads(self.upvotes)
		return username in ups["upvoters"]

	def upvote_nums(self):
		ups = json.loads(self.upvotes)
		return len(ups["upvoters"])