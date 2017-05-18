# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0018_auto_20170512_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movieinvolvement',
            name='role',
            field=models.CharField(max_length=3, choices=[(b'pra', b'Productora'), (b'dis', b'Distribuidora'), (b'pro', b'Productor'), (b'dir', b'Director'), (b'gui', b'Guionista'), (b'act', b'Actor'), (b'pre', b'Presentador')]),
        ),
        migrations.AlterField(
            model_name='seriesinvolvement',
            name='role',
            field=models.CharField(max_length=3, choices=[(b'pra', b'Productora'), (b'dis', b'Distribuidora'), (b'pro', b'Productor'), (b'dir', b'Director'), (b'gui', b'Guionista'), (b'act', b'Actor'), (b'pre', b'Presentador')]),
        ),
    ]
