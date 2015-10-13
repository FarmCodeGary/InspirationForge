# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20151005_1220'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=30, default='', null=True),
            preserve_default=False,
        ),
    ]
