# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0014_auto_20170303_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(to='items.Genre', blank=True),
        ),
        migrations.AlterField(
            model_name='comic',
            name='genres',
            field=models.ManyToManyField(to='items.Genre', blank=True),
        ),
        migrations.AlterField(
            model_name='comicseries',
            name='genres',
            field=models.ManyToManyField(to='items.Genre', blank=True),
        ),
        migrations.AlterField(
            model_name='dlc',
            name='genres',
            field=models.ManyToManyField(to='items.Genre', blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='genres',
            field=models.ManyToManyField(to='items.Genre', blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(to='items.Genre', blank=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='genres',
            field=models.ManyToManyField(to='items.Genre', blank=True),
        ),
    ]
