# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def make_default_category(apps, schema_editor):
    CategoryModel = apps.get_model('blog', 'Category')
    blog_category = CategoryModel.objects.create(name="Blog", slug="blog")
    ArticleModel = apps.get_model('blog', 'Article')
    for article in ArticleModel.objects.all():
        article.category = blog_category
        article.save()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20151215_1307'),
    ]

    operations = [
        migrations.RunPython(make_default_category,
            reverse_code=migrations.RunPython.noop),
    ]
