# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_auto_20161108_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinvolvement',
            name='role',
            field=models.CharField(max_length=3, choices=[(b'esc', b'Escritor'), (b'ilu', b'Ilustrador'), (b'tra', b'Traductor'), (b'edi', b'Editorial')]),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='option',
            field=models.CharField(max_length=3, choices=[(b'lei', b'Le\xc3\xaddo'), (b'pen', b'Pendiente'), (b'ley', b'Leyendo'), (b'pau', b'Pausado')]),
        ),
        migrations.AlterField(
            model_name='comicinvolvement',
            name='role',
            field=models.CharField(max_length=3, choices=[(b'edi', b'Editorial'), (b'gui', b'Guionista'), (b'dib', b'Dibujante')]),
        ),
        migrations.AlterField(
            model_name='comicmark',
            name='option',
            field=models.CharField(max_length=3, choices=[(b'fin', b'Finalizado'), (b'pen', b'Pendiente'), (b'sig', b'Siguiendo'), (b'pau', b'Pausado')]),
        ),
        migrations.AlterField(
            model_name='dlcinvolvement',
            name='role',
            field=models.CharField(max_length=3, choices=[(b'des', b'Desarrollador'), (b'dis', b'Distribuidor')]),
        ),
        migrations.AlterField(
            model_name='dlcmark',
            name='option',
            field=models.CharField(max_length=3, choices=[(b'ter', b'Terminado'), (b'com', b'Completado'), (b'pen', b'Pendiente'), (b'jug', b'Jugando'), (b'pau', b'Pausado')]),
        ),
        migrations.AlterField(
            model_name='gameinvolvement',
            name='role',
            field=models.CharField(max_length=3, choices=[(b'des', b'Desarrollador'), (b'dis', b'Distribuidor')]),
        ),
        migrations.AlterField(
            model_name='gamemark',
            name='option',
            field=models.CharField(max_length=3, choices=[(b'ter', b'Terminado'), (b'com', b'Completado'), (b'pen', b'Pendiente'), (b'jug', b'Jugando'), (b'pau', b'Pausado')]),
        ),
        migrations.AlterField(
            model_name='graphicnovelinvolvement',
            name='role',
            field=models.CharField(max_length=3, choices=[(b'edi', b'Editorial'), (b'gui', b'Guionista'), (b'dib', b'Dibujante')]),
        ),
        migrations.AlterField(
            model_name='graphicnovelmark',
            name='option',
            field=models.CharField(max_length=3, choices=[(b'lei', b'Le\xc3\xaddo'), (b'pen', b'Pendiente'), (b'ley', b'Leyendo'), (b'pau', b'Pausado')]),
        ),
        migrations.AlterField(
            model_name='movie',
            name='category',
            field=models.CharField(max_length=3, choices=[(b'pel', b'Pel\xc3\xadcula'), (b'cor', b'Corto'), (b'doc', b'Docufilm')]),
        ),
        migrations.AlterField(
            model_name='movieinvolvement',
            name='role',
            field=models.CharField(max_length=3, choices=[(b'pra', b'Productora'), (b'dis', b'Distribuidora'), (b'pro', b'Productora'), (b'dir', b'Director'), (b'gui', b'Guionista'), (b'act', b'Actor'), (b'pre', b'Presentador')]),
        ),
        migrations.AlterField(
            model_name='moviemark',
            name='option',
            field=models.CharField(max_length=3, choices=[(b'vis', b'Visto'), (b'pen', b'Pendiente')]),
        ),
        migrations.AlterField(
            model_name='series',
            name='category',
            field=models.CharField(max_length=3, choices=[(b'ser', b'Serie'), (b'min', b'Miniserie'), (b'pro', b'Programa de TV'), (b'doc', b'Documental')]),
        ),
        migrations.AlterField(
            model_name='series',
            name='status',
            field=models.CharField(max_length=3, choices=[(b'emi', b'En emisi\xc3\xb3n'), (b'can', b'Cancelado'), (b'fin', b'Finalizado'), (b'esp', b'A espera de nueva temporada')]),
        ),
        migrations.AlterField(
            model_name='seriesinvolvement',
            name='role',
            field=models.CharField(max_length=3, choices=[(b'pra', b'Productora'), (b'dis', b'Distribuidora'), (b'pro', b'Productora'), (b'dir', b'Director'), (b'gui', b'Guionista'), (b'act', b'Actor'), (b'pre', b'Presentador')]),
        ),
        migrations.AlterField(
            model_name='seriesmark',
            name='option',
            field=models.CharField(max_length=3, choices=[(b'fin', b'Finalizado'), (b'pen', b'Pendiente'), (b'sig', b'Siguiendo'), (b'pau', b'Pausado')]),
        ),
    ]
