# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20151217_1753'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='rendered_text',
            new_name='rendered_content',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='source_text',
            new_name='content_source',
        ),
        migrations.RenameField(
            model_name='contributor',
            old_name='rendered_text',
            new_name='rendered_content',
        ),
        migrations.RenameField(
            model_name='contributor',
            old_name='source_text',
            new_name='content_source',
        ),
    ]
