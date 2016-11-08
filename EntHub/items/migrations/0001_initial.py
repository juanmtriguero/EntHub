# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('bio', models.TextField(blank=True)),
                ('image', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
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
            name='BookInvolvement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=3, choices=[(b'esc', b'escritor'), (b'ilu', b'ilustrador'), (b'tra', b'traductor'), (b'edi', b'editorial')])),
                ('agent', models.ForeignKey(to='items.Agent')),
                ('book', models.ForeignKey(to='items.Book')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BookMark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)])),
                ('fav', models.BooleanField(default=False)),
                ('option', models.CharField(max_length=3, choices=[(b'lei', b'le\xc3\xaddo'), (b'pen', b'pendiente'), (b'ley', b'leyendo'), (b'pau', b'pausado')])),
                ('book', models.ForeignKey(to='items.Book')),
                ('user', models.ForeignKey(to='main.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DLC',
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
            name='DLCInvolvement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=3, choices=[(b'des', b'desarrollador'), (b'dis', b'distribuidor')])),
                ('agent', models.ForeignKey(to='items.Agent')),
                ('dlc', models.ForeignKey(to='items.DLC')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DLCMark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)])),
                ('fav', models.BooleanField(default=False)),
                ('option', models.CharField(max_length=3, choices=[(b'ter', b'terminado'), (b'com', b'completado'), (b'pen', b'pendiente'), (b'jug', b'jugando'), (b'pau', b'pausado')])),
                ('dlc', models.ForeignKey(to='items.DLC')),
                ('user', models.ForeignKey(to='main.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Game',
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
            name='GameInvolvement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=3, choices=[(b'des', b'desarrollador'), (b'dis', b'distribuidor')])),
                ('agent', models.ForeignKey(to='items.Agent')),
                ('game', models.ForeignKey(to='items.Game')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameMark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)])),
                ('fav', models.BooleanField(default=False)),
                ('option', models.CharField(max_length=3, choices=[(b'ter', b'terminado'), (b'com', b'completado'), (b'pen', b'pendiente'), (b'jug', b'jugando'), (b'pau', b'pausado')])),
                ('game', models.ForeignKey(to='items.Game')),
                ('user', models.ForeignKey(to='main.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('creator', models.ForeignKey(related_name='creator', to='main.Account')),
                ('followers', models.ManyToManyField(related_name='follower', to='main.Account', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('short', models.CharField(max_length=5)),
                ('image', models.URLField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='agents',
            field=models.ManyToManyField(to='items.Agent', through='items.GameInvolvement'),
        ),
        migrations.AddField(
            model_name='game',
            name='genres',
            field=models.ManyToManyField(to='items.Genre'),
        ),
        migrations.AddField(
            model_name='game',
            name='lists',
            field=models.ManyToManyField(to='items.List', blank=True),
        ),
        migrations.AddField(
            model_name='game',
            name='platforms',
            field=models.ManyToManyField(to='items.Platform'),
        ),
        migrations.AddField(
            model_name='dlc',
            name='agents',
            field=models.ManyToManyField(to='items.Agent', through='items.DLCInvolvement'),
        ),
        migrations.AddField(
            model_name='dlc',
            name='game',
            field=models.ForeignKey(to='items.Game'),
        ),
        migrations.AddField(
            model_name='dlc',
            name='genres',
            field=models.ManyToManyField(to='items.Genre'),
        ),
        migrations.AddField(
            model_name='dlc',
            name='lists',
            field=models.ManyToManyField(to='items.List', blank=True),
        ),
        migrations.AddField(
            model_name='dlc',
            name='platforms',
            field=models.ManyToManyField(to='items.Platform'),
        ),
        migrations.AddField(
            model_name='book',
            name='agents',
            field=models.ManyToManyField(to='items.Agent', through='items.BookInvolvement'),
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(to='items.Genre'),
        ),
        migrations.AddField(
            model_name='book',
            name='lists',
            field=models.ManyToManyField(to='items.List', blank=True),
        ),
    ]
