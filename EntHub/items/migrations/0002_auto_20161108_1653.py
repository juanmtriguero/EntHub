# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comic',
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
            name='ComicInvolvement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=3, choices=[(b'edi', b'editorial'), (b'gui', b'guionista'), (b'dib', b'dibujante')])),
                ('agent', models.ForeignKey(to='items.Agent')),
                ('comic', models.ForeignKey(to='items.Comic')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ComicMark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)])),
                ('fav', models.BooleanField(default=False)),
                ('option', models.CharField(max_length=3, choices=[(b'fin', b'finalizado'), (b'pen', b'pendiente'), (b'sig', b'siguiendo'), (b'pau', b'pausado')])),
                ('comic', models.ForeignKey(to='items.Comic')),
                ('user', models.ForeignKey(to='main.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GraphicNovel',
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
            name='GraphicNovelInvolvement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=3, choices=[(b'edi', b'editorial'), (b'gui', b'guionista'), (b'dib', b'dibujante')])),
                ('agent', models.ForeignKey(to='items.Agent')),
                ('graphicNovel', models.ForeignKey(to='items.GraphicNovel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GraphicNovelMark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)])),
                ('fav', models.BooleanField(default=False)),
                ('option', models.CharField(max_length=3, choices=[(b'lei', b'le\xc3\xaddo'), (b'pen', b'pendiente'), (b'ley', b'leyendo'), (b'pau', b'pausado')])),
                ('graphicNovel', models.ForeignKey(to='items.GraphicNovel')),
                ('user', models.ForeignKey(to='main.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Number',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=100, blank=True)),
                ('comic', models.ForeignKey(to='items.Comic')),
                ('tics', models.ManyToManyField(to='main.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='graphicnovel',
            name='agents',
            field=models.ManyToManyField(to='items.Agent', through='items.GraphicNovelInvolvement'),
        ),
        migrations.AddField(
            model_name='graphicnovel',
            name='genres',
            field=models.ManyToManyField(to='items.Genre'),
        ),
        migrations.AddField(
            model_name='graphicnovel',
            name='lists',
            field=models.ManyToManyField(to='items.List', blank=True),
        ),
        migrations.AddField(
            model_name='comic',
            name='agents',
            field=models.ManyToManyField(to='items.Agent', through='items.ComicInvolvement'),
        ),
        migrations.AddField(
            model_name='comic',
            name='genres',
            field=models.ManyToManyField(to='items.Genre'),
        ),
        migrations.AddField(
            model_name='comic',
            name='lists',
            field=models.ManyToManyField(to='items.List', blank=True),
        ),
    ]
