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

class GraphicNovel(Item):
	agents = models.ManyToManyField(Agent, through="GraphicNovelInvolvement")

class Comic(Item):
	agents = models.ManyToManyField(Agent, through="ComicInvolvement")

# TODO all items

# Sub-items

class Subitem(models.Model):
	number = models.IntegerField()
	name = models.CharField(max_length=100, blank=True)
	tics = models.ManyToManyField(Account)

	class Meta:
		abstract = True

	def __unicode__(self):
		return unicode(self.number) + " - " + unicode(self.name)

class Number(Subitem):
	comic = models.ForeignKey(Comic, on_delete=models.CASCADE)

# TODO sub-items

# Marks

class Mark(models.Model):
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	rating = models.IntegerField(blank=True, choices=
		[(i, i) for i in range(1,5)])
	fav = models.BooleanField(default=False)

	class Meta:
		abstract = True

class IndividualMark(Mark):
	OPTION_CHOICES = (
		('lei', 'leído'),
		('pen', 'pendiente'),
		('ley', 'leyendo'),
		('pau', 'pausado'),
	)
	option = models.CharField(max_length=3, choices=OPTION_CHOICES)

	class Meta:
		abstract = True

class BookMark(IndividualMark):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)

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

class GraphicNovelMark(IndividualMark):
	graphicNovel = models.ForeignKey(GraphicNovel, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.user) + " ha marcado la novela gráfica "\
			   + unicode(self.graphicNovel) + " como " + unicode(self.get_option_display())

class GroupMark(Mark):
	OPTION_CHOICES = (
		('fin', 'finalizado'),
		('pen', 'pendiente'),
		('sig', 'siguiendo'),
		('pau', 'pausado'),
	)
	option = models.CharField(max_length=3, choices=OPTION_CHOICES)

	class Meta:
		abstract = True

class ComicMark(GroupMark):
	comic = models.ForeignKey(Comic, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el cómic "\
			   + unicode(self.comic) + " como " + unicode(self.get_option_display())

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

class GameItemInvolvement(Involvement):
	ROLE_CHOICES = (
		('des', 'desarrollador'),
		('dis', 'distribuidor'),
	)
	role = models.CharField(max_length=3, choices=ROLE_CHOICES)

	class Meta:
		abstract = True

class GameInvolvement(GameItemInvolvement):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.agent) + " aparece en el juego "\
			   + unicode(self.game) + " como " + unicode(self.get_role_display())

class DLCInvolvement(GameItemInvolvement):
	dlc = models.ForeignKey(DLC, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.agent) + " aparece en el DLC "\
			   + unicode(self.dlc) + " como " + unicode(self.get_role_display())

class ComicItemInvolvement(Involvement):
	ROLE_CHOICES = (
		('edi', 'editorial'),
		('gui', 'guionista'),
		('dib', 'dibujante'),
	)
	role = models.CharField(max_length=3, choices=ROLE_CHOICES)

	class Meta:
		abstract = True

class GraphicNovelInvolvement(ComicItemInvolvement):
	graphicNovel = models.ForeignKey(GraphicNovel, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.agent) + " aparece en la novela gráfica "\
			   + unicode(self.graphicNovel) + " como " + unicode(self.get_role_display())

class ComicInvolvement(ComicItemInvolvement):
	comic = models.ForeignKey(Comic, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.agent) + " aparece en el cómic "\
			   + unicode(self.comic) + " como " + unicode(self.get_role_display())

# TODO all involvements
