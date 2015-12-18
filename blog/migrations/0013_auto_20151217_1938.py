# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20151217_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='content_source',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='rendered_content',
            field=models.TextField(editable=False, blank=True),
        ),
    ]
