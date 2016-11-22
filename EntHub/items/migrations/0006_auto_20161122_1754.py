# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_auto_20161122_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='category',
            field=models.CharField(default=b'pel', max_length=3, choices=[(b'pel', b'Pel\xc3\xadcula'), (b'cor', b'Corto'), (b'doc', b'Docufilm')]),
        ),
        migrations.AlterField(
            model_name='series',
            name='category',
            field=models.CharField(default=b'ser', max_length=3, choices=[(b'ser', b'Serie'), (b'min', b'Miniserie'), (b'pro', b'Programa de TV'), (b'doc', b'Documental')]),
        ),
        migrations.AlterField(
            model_name='series',
            name='status',
            field=models.CharField(default=b'emi', max_length=3, choices=[(b'emi', b'En emisi\xc3\xb3n'), (b'can', b'Cancelado'), (b'fin', b'Finalizado'), (b'esp', b'A espera de nueva temporada')]),
        ),
    ]
