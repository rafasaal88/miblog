from django.db import models
from django.contrib.auth.models import User
from django_markdown.models import MarkdownField
# Create your models here.

class Entry(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=200)
	body = models.TextField()
	publicado = models.SlugField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(User)

	def __unicode__(self):
		return self.title

class Comentario(models.Model):
	id = models.AutoField(primary_key=True)
	entry = models.ForeignKey(Entry)
	user = models.ForeignKey(User, null=True, default=None)
	title = models.CharField(max_length=200)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title

class Mensaje(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, null=True, default=None)
	title = models.CharField(max_length=200)
	body = models.TextField()
	addressee = models.CharField(max_length=200)	
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title

class Perfil(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, null=True, default=None)
	twitter = models.CharField(max_length=250, blank=True)
	avatar = models.ImageField(upload_to='avatares')
	created = models.DateTimeField(auto_now_add=True)

