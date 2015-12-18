# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def copy_description_into_content_source(apps, schema_editor):
    CategoryModel = apps.get_model('blog', 'Category')
    for category in CategoryModel.objects.all():
        category.content_source = category.description
        category.save()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20151217_1938'),
    ]

    operations = [
        migrations.RunPython(copy_description_into_content_source,
            reverse_code=migrations.RunPython.noop),
    ]
