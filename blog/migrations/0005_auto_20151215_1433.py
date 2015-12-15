# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20151215_1308'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AddField(
            model_name='article',
            name='enclosure_length',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='enclosure_mime_type',
            field=models.CharField(blank=True, max_length=50, choices=[('audio/mpeg', 'audio/mpeg (e.g. MP3)')]),
        ),
        migrations.AddField(
            model_name='article',
            name='enclosure_url',
            field=models.URLField(blank=True),
        ),
    ]
