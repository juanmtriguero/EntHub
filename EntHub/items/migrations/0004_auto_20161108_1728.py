# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        ('items', '0003_auto_20161108_1703'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=100, blank=True)),
                ('season', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('description', models.TextField(blank=True)),
                ('image', models.URLField(blank=True)),
                ('rating', models.FloatField(default=0.0)),
                ('count', models.IntegerField(default=0)),
                ('category', models.CharField(max_length=3, choices=[(b'pel', b'pel\xc3\xadcula'), (b'cor', b'corto'), (b'doc', b'docufilm')])),
                ('duration', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MovieInvolvement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=3, choices=[(b'pra', b'productora'), (b'dis', b'distribuidora'), (b'pro', b'productora'), (b'dir', b'director'), (b'gui', b'guionista'), (b'act', b'actor'), (b'pre', b'presentador')])),
                ('agent', models.ForeignKey(to='items.Agent')),
                ('movie', models.ForeignKey(to='items.Movie')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MovieMark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('fav', models.BooleanField(default=False)),
                ('option', models.CharField(max_length=3, choices=[(b'vis', b'visto'), (b'pen', b'pendiente')])),
                ('movie', models.ForeignKey(to='items.Movie')),
                ('user', models.ForeignKey(to='main.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('description', models.TextField(blank=True)),
                ('image', models.URLField(blank=True)),
                ('rating', models.FloatField(default=0.0)),
                ('count', models.IntegerField(default=0)),
                ('category', models.CharField(max_length=3, choices=[(b'ser', b'serie'), (b'min', b'miniserie'), (b'pro', b'programa de TV'), (b'doc', b'documental')])),
                ('status', models.CharField(max_length=3, choices=[(b'emi', b'en emisi\xc3\xb3n'), (b'can', b'cancelado'), (b'fin', b'finalizado'), (b'esp', b'a espera de nueva temporada')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SeriesInvolvement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=3, choices=[(b'pra', b'productora'), (b'dis', b'distribuidora'), (b'pro', b'productora'), (b'dir', b'director'), (b'gui', b'guionista'), (b'act', b'actor'), (b'pre', b'presentador')])),
                ('agent', models.ForeignKey(to='items.Agent')),
                ('series', models.ForeignKey(to='items.Series')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SeriesMark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('fav', models.BooleanField(default=False)),
                ('option', models.CharField(max_length=3, choices=[(b'fin', b'finalizado'), (b'pen', b'pendiente'), (b'sig', b'siguiendo'), (b'pau', b'pausado')])),
                ('series', models.ForeignKey(to='items.Series')),
                ('user', models.ForeignKey(to='main.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='series',
            name='agents',
            field=models.ManyToManyField(to='items.Agent', through='items.SeriesInvolvement'),
        ),
        migrations.AddField(
            model_name='series',
            name='genres',
            field=models.ManyToManyField(to='items.Genre'),
        ),
        migrations.AddField(
            model_name='series',
            name='lists',
            field=models.ManyToManyField(to='items.List', blank=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='agents',
            field=models.ManyToManyField(to='items.Agent', through='items.MovieInvolvement'),
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(to='items.Genre'),
        ),
        migrations.AddField(
            model_name='movie',
            name='lists',
            field=models.ManyToManyField(to='items.List', blank=True),
        ),
        migrations.AddField(
            model_name='chapter',
            name='series',
            field=models.ForeignKey(to='items.Series'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='tics',
            field=models.ManyToManyField(to='main.Account'),
        ),
    ]
