# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20161116_1512'),
        ('items', '0008_auto_20161123_2032'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComicSeries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('description', models.TextField(blank=True)),
                ('image', models.URLField(blank=True)),
                ('rating', models.FloatField(default=0.0)),
                ('count', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ComicSeriesInvolvement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=3, choices=[(b'edi', b'Editorial'), (b'gui', b'Guionista'), (b'dib', b'Dibujante')])),
                ('agent', models.ForeignKey(to='items.Agent')),
                ('comic', models.ForeignKey(to='items.ComicSeries')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ComicSeriesMark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('fav', models.BooleanField(default=False)),
                ('option', models.CharField(max_length=3, choices=[(b'fin', b'Finalizado'), (b'pen', b'Pendiente'), (b'sig', b'Siguiendo'), (b'pau', b'Pausado')])),
                ('comic', models.ForeignKey(to='items.ComicSeries')),
                ('user', models.ForeignKey(to='main.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='graphicnovel',
            name='agents',
        ),
        migrations.RemoveField(
            model_name='graphicnovel',
            name='genres',
        ),
        migrations.RemoveField(
            model_name='graphicnovel',
            name='lists',
        ),
        migrations.RemoveField(
            model_name='graphicnovelinvolvement',
            name='agent',
        ),
        migrations.RemoveField(
            model_name='graphicnovelinvolvement',
            name='graphicNovel',
        ),
        migrations.RemoveField(
            model_name='graphicnovelmark',
            name='graphicNovel',
        ),
        migrations.RemoveField(
            model_name='graphicnovelmark',
            name='user',
        ),
        migrations.AlterField(
            model_name='comicmark',
            name='option',
            field=models.CharField(max_length=3, choices=[(b'lei', b'Le\xc3\xaddo'), (b'pen', b'Pendiente'), (b'ley', b'Leyendo'), (b'pau', b'Pausado')]),
        ),
        migrations.AlterField(
            model_name='number',
            name='comic',
            field=models.ForeignKey(to='items.ComicSeries'),
        ),
        migrations.DeleteModel(
            name='GraphicNovel',
        ),
        migrations.DeleteModel(
            name='GraphicNovelInvolvement',
        ),
        migrations.DeleteModel(
            name='GraphicNovelMark',
        ),
        migrations.AddField(
            model_name='comicseries',
            name='agents',
            field=models.ManyToManyField(to='items.Agent', through='items.ComicSeriesInvolvement'),
        ),
        migrations.AddField(
            model_name='comicseries',
            name='genres',
            field=models.ManyToManyField(to='items.Genre'),
        ),
        migrations.AddField(
            model_name='comicseries',
            name='lists',
            field=models.ManyToManyField(to='items.List', blank=True),
        ),
    ]
