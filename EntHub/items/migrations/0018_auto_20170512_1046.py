# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0017_auto_20170422_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dlc',
            name='platforms',
            field=models.ManyToManyField(to='items.Platform', blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='platforms',
            field=models.ManyToManyField(to='items.Platform', blank=True),
        ),
    ]
