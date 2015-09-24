# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20150923_2015'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=30)),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published', default=django.utils.timezone.now)),
                ('article', models.ForeignKey(to='blog.Article')),
            ],
        ),
    ]
