# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.text import slugify

def generate_tag_slug(apps, schema_editor):
    Tag = apps.get_model("blog", "Tag")
    for tag in Tag.objects.all():
        tag.slug = slugify(tag.name)
        tag.save()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20151005_1437'),
    ]

    operations = [
        migrations.RunPython(generate_tag_slug)
    ]
