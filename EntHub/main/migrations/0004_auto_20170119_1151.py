# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_account_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='following',
            field=models.ManyToManyField(related_name='followers', to='main.Account', blank=True),
        ),
    ]
