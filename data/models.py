from django.db import models

class Article(models.Model):
	link = models.TextField()
	title = models.TextField()
	date = models.DateTimeField()
	author = models.CharField(max_length=100)

class Lookup(models.Model):
	last = models.DateTimeField()