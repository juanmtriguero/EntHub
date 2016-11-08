#encoding:utf-8

from django.db import models
from main.models import Account

# Genre

class Genre(models.Model):
	name = models.CharField(max_length=20)

	def __unicode__(self):
		return unicode(self.name)

# Agent

class Agent(models.Model):
	name = models.CharField(max_length=50)
	bio = models.TextField(blank=True)
	image = models.URLField(blank=True)

	def __unicode__(self):
		return unicode(self.name)

# Platform

class Platform(models.Model):
	name = models.CharField(max_length=50)
	short = models.CharField(max_length=5)
	image = models.URLField(blank=True)

	def __unicode__(self):
		return unicode(self.name)

#List

class List(models.Model):
	name = models.CharField(max_length=100)
	creator = models.ForeignKey(Account, related_name="creator", on_delete=models.CASCADE)
	followers = models.ManyToManyField(Account, related_name="follower", blank=True)

	def __unicode__(self):
		return unicode(self.name)

# Items

class Item(models.Model):
	title = models.CharField(max_length=100)
	year = models.IntegerField()
	description = models.TextField(blank=True)
	image = models.URLField(blank=True)
	rating = models.FloatField(default=0.0)
	count = models.IntegerField(default=0)
	genres = models.ManyToManyField(Genre)
	lists = models.ManyToManyField(List, blank=True)

	class Meta:
		abstract = True

	def __unicode__(self):
		return unicode(self.title) + " ("\
			   + unicode(self.year) + ")"

class Book(Item):
	agents = models.ManyToManyField(Agent, through="BookInvolvement")

class GameItem(Item):
	platforms = models.ManyToManyField(Platform)

	class Meta:
		abstract = True

class Game(GameItem):
	agents = models.ManyToManyField(Agent, through="GameInvolvement")

class DLC(GameItem):
	agents = models.ManyToManyField(Agent, through="DLCInvolvement")
	game = models.ForeignKey(Game, on_delete=models.CASCADE)

# TODO all items

# Sub-items

# TODO sub-items

# Marks

class Mark(models.Model):
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	rating = models.IntegerField(blank=True, choices=
		[(i, i) for i in range(1,5)])
	fav = models.BooleanField(default=False)

	class Meta:
		abstract = True

class BookMark(Mark):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	OPTION_CHOICES = (
		('lei', 'leído'),
		('pen', 'pendiente'),
		('ley', 'leyendo'),
		('pau', 'pausado'),
	)
	option = models.CharField(max_length=3, choices=OPTION_CHOICES)

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el libro "\
			   + unicode(self.book) + " como " + unicode(self.get_option_display())

class PlayableMark(Mark):
	OPTION_CHOICES = (
		('ter', 'terminado'),
		('com', 'completado'),
		('pen', 'pendiente'),
		('jug', 'jugando'),
		('pau', 'pausado'),
	)
	option = models.CharField(max_length=3, choices=OPTION_CHOICES)

	class Meta:
		abstract = True

class GameMark(PlayableMark):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el juego "\
			   + unicode(self.game) + " como " + unicode(self.get_option_display())

class DLCMark(PlayableMark):
	dlc = models.ForeignKey(DLC, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el DLC "\
			   + unicode(self.dlc) + " como " + unicode(self.get_option_display())

# TODO all marks

# Involvements

class Involvement(models.Model):
	agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

	class Meta:
		abstract = True

class BookInvolvement(Involvement):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	ROLE_CHOICES = (
		('esc', 'escritor'),
		('ilu', 'ilustrador'),
		('tra', 'traductor'),
		('edi', 'editorial'),
	)
	role = models.CharField(max_length=3, choices=ROLE_CHOICES)

	def __unicode__(self):
		return unicode(self.agent) + " aparece en el libro "\
			   + unicode(self.book) + " como " + unicode(self.get_role_display())

class GameInvolvement(Involvement):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	ROLE_CHOICES = (
		('des', 'desarrollador'),
		('dis', 'distribuidor'),
	)
	role = models.CharField(max_length=3, choices=ROLE_CHOICES)

	def __unicode__(self):
		return unicode(self.agent) + " aparece en el juego "\
			   + unicode(self.game) + " como " + unicode(self.get_role_display())

class DLCInvolvement(Involvement):
	dlc = models.ForeignKey(DLC, on_delete=models.CASCADE)
	ROLE_CHOICES = (
		('des', 'desarrollador'),
		('dis', 'distribuidor'),
	)
	role = models.CharField(max_length=3, choices=ROLE_CHOICES)

	def __unicode__(self):
		return unicode(self.agent) + " aparece en el DLC "\
			   + unicode(self.dlc) + " como " + unicode(self.get_role_display())

# TODO all involvements
