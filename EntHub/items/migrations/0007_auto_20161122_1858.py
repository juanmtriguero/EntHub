# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_auto_20161122_1754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='tics',
        ),
        migrations.RemoveField(
            model_name='number',
            name='tics',
        ),
    ]
