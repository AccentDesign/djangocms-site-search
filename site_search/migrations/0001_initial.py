# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('pub_date', models.DateTimeField(null=True)),
                ('login_required', models.BooleanField()),
                ('description', models.TextField(null=True, blank=True)),
                ('url', models.URLField()),
                ('search_text', models.TextField(null=True, blank=True)),
                ('language', models.CharField(max_length=255)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
        ),
    ]
