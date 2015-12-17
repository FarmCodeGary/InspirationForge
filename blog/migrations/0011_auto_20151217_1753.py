# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20151217_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributor',
            name='rendered_text',
            field=models.TextField(editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='contributor',
            name='source_text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='rendered_text',
            field=models.TextField(editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='source_text',
            field=models.TextField(blank=True),
        ),
    ]
