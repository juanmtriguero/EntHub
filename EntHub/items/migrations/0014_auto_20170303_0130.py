# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0013_auto_20170215_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='category',
            field=models.CharField(default=b'ser', max_length=3, choices=[(b'ser', b'Serie'), (b'min', b'Miniserie'), (b'pro', b'Programa TV'), (b'doc', b'Documental')]),
        ),
    ]
