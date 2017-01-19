# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0009_auto_20161125_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='option',
            field=models.CharField(max_length=3, choices=[(b'pen', b'Pendiente'), (b'ley', b'Leyendo'), (b'pau', b'Pausado'), (b'lei', b'Le\xc3\xaddo')]),
        ),
        migrations.AlterField(
            model_name='comicmark',
            name='option',
            field=models.CharField(max_length=3, choices=[(b'pen', b'Pendiente'), (b'ley', b'Leyendo'), (b'pau', b'Pausado'), (b'lei', b'Le\xc3\xaddo')]),
        ),
        migrations.AlterField(
            model_name='comicseriesmark',
            name='option',
            field=models.CharField(max_length=3, choices=[(b'pen', b'Pendiente'), (b'sig', b'Siguiendo'), (b'pau', b'Pausado'), (b'fin', b'Finalizado')]),
        ),
        migrations.AlterField(
            model_name='dlcmark',
            name='option',
            field=models.CharField(max_length=3, choices=[(b'pen', b'Pendiente'), (b'jug', b'Jugando'), (b'pau', b'Pausado'), (b'ter', b'Terminado'), (b'com', b'Completado')]),
        ),
        migrations.AlterField(
            model_name='gamemark',
            name='option',
            field=models.CharField(max_length=3, choices=[(b'pen', b'Pendiente'), (b'jug', b'Jugando'), (b'pau', b'Pausado'), (b'ter', b'Terminado'), (b'com', b'Completado')]),
        ),
        migrations.AlterField(
            model_name='moviemark',
            name='option',
            field=models.CharField(max_length=3, choices=[(b'pen', b'Pendiente'), (b'vis', b'Visto')]),
        ),
        migrations.AlterField(
            model_name='seriesmark',
            name='option',
            field=models.CharField(max_length=3, choices=[(b'pen', b'Pendiente'), (b'sig', b'Siguiendo'), (b'pau', b'Pausado'), (b'fin', b'Finalizado')]),
        ),
    ]
