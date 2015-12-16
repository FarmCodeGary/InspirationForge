# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20151216_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='contributors',
            field=models.ManyToManyField(to='blog.Contributor'),
        ),
    ]
