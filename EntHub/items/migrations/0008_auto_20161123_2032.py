# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0007_auto_20161122_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='number',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
