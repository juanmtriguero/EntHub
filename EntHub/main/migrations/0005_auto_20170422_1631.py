# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_followinglog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followinglog',
            name='follower',
            field=models.ForeignKey(related_name='following_logs', to='main.Account'),
        ),
        migrations.AlterField(
            model_name='followinglog',
            name='following',
            field=models.ForeignKey(related_name='f_logs+', to='main.Account'),
        ),
    ]
