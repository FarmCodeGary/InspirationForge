# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_auto_20151215_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('display_name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(to='blog.Category', default=1),
        ),
    ]
