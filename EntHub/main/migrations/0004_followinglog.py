# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_account_following'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowingLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('follower', models.ForeignKey(related_name='subject', to='main.Account')),
                ('following', models.ForeignKey(related_name='object+', to='main.Account')),
            ],
        ),
    ]
