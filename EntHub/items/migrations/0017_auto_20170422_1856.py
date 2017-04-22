# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0016_bookmarklog_comicmarklog_comicseriesmarklog_dlcmarklog_gamemarklog_moviemarklog_seriesmarklog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comicseriesmarklog',
            old_name='comic',
            new_name='comicseries',
        ),
    ]
