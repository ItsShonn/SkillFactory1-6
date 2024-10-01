from django.db import models
from datetime import datetime
from datetime import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
	username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	rating = models.IntegerField(default=0, null=True)

	def update_rating(self):
		res = 0
		for post in Post.objects.filter(author=self).values('rating'):
			res += post.get('rating') * 3

		for comment in Comment.objects.filter(username=self.username.id).values('rating'):
			res += comment.get('rating')

		for a_post in Post.objects.filter(author=self).values('id'):
			for comment in Comment.objects.filter(post=a_post.get('id')).values('rating'):
				res += comment.get('rating')

		self.rating = res
		self.save()

	def __str__(self):
		return self.username.username


class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)
	subscribers = models.ManyToManyField(User, through='UserToCategory')

	def __str__(self):
		return self.name


class UserToCategory(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
	news = 'N'
	article = 'A'
	CHOICE = [(news, 'News'), (article, 'Article')]

	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	type = models.CharField(choices=CHOICE, max_length=1)
	date = models.DateTimeField(auto_now=True)
	categories = models.ManyToManyField(Category, through='PostCategory')
	title = models.CharField(max_length=255)
	content = models.TextField()
	rating = models.IntegerField(default=0, null=True)

	def like(self):
		self.rating += 1
		self.save()

	def dislike(self):
		self.rating -= 1
		self.save()

	def preview(self):
		return self.content[:124] + "..."

	def get_absolute_url(self):
		return reverse('news_detail', args=[str(self.id)])


class PostCategory(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	username = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	date = models.DateTimeField(auto_now=True)
	rating = models.IntegerField(default=0, null=True)

	def like(self):
		self.rating += 1
		self.save()

	def dislike(self):
		self.rating -= 1
		self.save()
