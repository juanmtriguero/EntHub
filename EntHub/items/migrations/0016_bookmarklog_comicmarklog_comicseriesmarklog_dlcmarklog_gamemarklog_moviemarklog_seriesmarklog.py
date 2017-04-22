# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('items', '0015_auto_20170328_1928'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookMarkLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('fav', models.BooleanField(default=False)),
                ('option', models.CharField(blank=True, max_length=3, choices=[(b'pen', b'Pendiente'), (b'ley', b'Leyendo'), (b'pau', b'Pausado'), (b'lei', b'Le\xc3\xaddo')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(related_name='+', to='items.Book')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ComicMarkLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('fav', models.BooleanField(default=False)),
                ('option', models.CharField(blank=True, max_length=3, choices=[(b'pen', b'Pendiente'), (b'ley', b'Leyendo'), (b'pau', b'Pausado'), (b'lei', b'Le\xc3\xaddo')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comic', models.ForeignKey(related_name='+', to='items.Comic')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ComicSeriesMarkLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('fav', models.BooleanField(default=False)),
                ('option', models.CharField(blank=True, max_length=3, choices=[(b'pen', b'Pendiente'), (b'sig', b'Siguiendo'), (b'pau', b'Pausado'), (b'fin', b'Finalizado')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comic', models.ForeignKey(related_name='+', to='items.ComicSeries')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DLCMarkLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('fav', models.BooleanField(default=False)),
                ('option', models.CharField(blank=True, max_length=3, choices=[(b'pen', b'Pendiente'), (b'jug', b'Jugando'), (b'pau', b'Pausado'), (b'ter', b'Terminado'), (b'com', b'Completado')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('dlc', models.ForeignKey(related_name='+', to='items.DLC')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameMarkLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('fav', models.BooleanField(default=False)),
                ('option', models.CharField(blank=True, max_length=3, choices=[(b'pen', b'Pendiente'), (b'jug', b'Jugando'), (b'pau', b'Pausado'), (b'ter', b'Terminado'), (b'com', b'Completado')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(related_name='+', to='items.Game')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MovieMarkLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('fav', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('option', models.CharField(blank=True, max_length=3, choices=[(b'pen', b'Pendiente'), (b'vis', b'Visto')])),
                ('movie', models.ForeignKey(related_name='+', to='items.Movie')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SeriesMarkLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('fav', models.BooleanField(default=False)),
                ('option', models.CharField(blank=True, max_length=3, choices=[(b'pen', b'Pendiente'), (b'sig', b'Siguiendo'), (b'pau', b'Pausado'), (b'fin', b'Finalizado')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('series', models.ForeignKey(related_name='+', to='items.Series')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
