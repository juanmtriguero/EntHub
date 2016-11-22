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

class Movie(Item):
	CATEGORY_CHOICES = (
		('pel', 'Película'),
		('cor', 'Corto'),
		('doc', 'Docufilm'),
	)
	category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default='pel')
	duration = models.IntegerField()
	agents = models.ManyToManyField(Agent, through="MovieInvolvement")

class Series(Item):
	CATEGORY_CHOICES = (
		('ser', 'Serie'),
		('min', 'Miniserie'),
		('pro', 'Programa de TV'),
		('doc', 'Documental'),
	)
	category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default='ser')
	STATUS_CHOICES = (
		('emi', 'En emisión'),
		('can', 'Cancelado'),
		('fin', 'Finalizado'),
		('esp', 'A espera de nueva temporada'),
	)
	status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='emi')
	agents = models.ManyToManyField(Agent, through="SeriesInvolvement")

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

class Chapter(Subitem):
	season = models.IntegerField()
	series = models.ForeignKey(Series, on_delete=models.CASCADE)

# Marks

class Mark(models.Model):
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	rating = models.IntegerField(null=True, blank=True, choices=
		[(i, i) for i in range(1,6)]) # TODO Update item rating
	fav = models.BooleanField(default=False)

	class Meta:
		abstract = True

class IndividualMark(Mark):
	OPTION_CHOICES = (
		('lei', 'Leído'),
		('pen', 'Pendiente'),
		('ley', 'Leyendo'),
		('pau', 'Pausado'),
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
		('ter', 'Terminado'),
		('com', 'Completado'),
		('pen', 'Pendiente'),
		('jug', 'Jugando'),
		('pau', 'Pausado'),
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
		('fin', 'Finalizado'),
		('pen', 'Pendiente'),
		('sig', 'Siguiendo'),
		('pau', 'Pausado'),
	)
	option = models.CharField(max_length=3, choices=OPTION_CHOICES)

	class Meta:
		abstract = True

class ComicMark(GroupMark):
	comic = models.ForeignKey(Comic, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el cómic "\
			   + unicode(self.comic) + " como " + unicode(self.get_option_display())

class SeriesMark(GroupMark):
	series = models.ForeignKey(Series, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el " + unicode(self.series.category)\
			   + " " + unicode(self.series) + " como " + unicode(self.get_option_display())

class MovieMark(Mark):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	OPTION_CHOICES = (
		('vis', 'Visto'),
		('pen', 'Pendiente'),
	)
	option = models.CharField(max_length=3, choices=OPTION_CHOICES)

	def __unicode__(self):
		return unicode(self.user) + " ha marcado el " + unicode(self.movie.category)\
			   + " " + unicode(self.movie) + " como " + unicode(self.get_option_display())

# Involvements

class Involvement(models.Model):
	agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

	class Meta:
		abstract = True

class BookInvolvement(Involvement):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	ROLE_CHOICES = (
		('esc', 'Escritor'),
		('ilu', 'Ilustrador'),
		('tra', 'Traductor'),
		('edi', 'Editorial'),
	)
	role = models.CharField(max_length=3, choices=ROLE_CHOICES)

	def __unicode__(self):
		return unicode(self.agent) + " aparece en el libro "\
			   + unicode(self.book) + " como " + unicode(self.get_role_display())

class GameItemInvolvement(Involvement):
	ROLE_CHOICES = (
		('des', 'Desarrollador'),
		('dis', 'Distribuidor'),
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
		('edi', 'Editorial'),
		('gui', 'Guionista'),
		('dib', 'Dibujante'),
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

class MovieItemInvolvement(Involvement):
	ROLE_CHOICES = (
		('pra', 'Productora'),
		('dis', 'Distribuidora'),
		('pro', 'Productora'),
		('dir', 'Director'),
		('gui', 'Guionista'),
		('act', 'Actor'),
		('pre', 'Presentador'),
	)
	role = models.CharField(max_length=3, choices=ROLE_CHOICES)

	class Meta:
		abstract = True

class MovieInvolvement(MovieItemInvolvement):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.agent) + " aparece en el " + unicode(self.movie.category)\
			   + " " + unicode(self.movie) + " como " + unicode(self.get_role_display())

class SeriesInvolvement(MovieItemInvolvement):
	series = models.ForeignKey(Series, on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.agent) + " aparece en el " + unicode(self.series.category)\
			   + " " + unicode(self.series) + " como " + unicode(self.get_role_display())