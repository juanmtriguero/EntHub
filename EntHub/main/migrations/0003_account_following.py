# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20161116_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='following',
            field=models.ManyToManyField(related_name='_account_following_+', to='main.Account', blank=True),
        ),
    ]
