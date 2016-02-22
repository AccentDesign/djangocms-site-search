# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValidSearchFieldsModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(
                    serialize=False, parent_link=True, auto_created=True,
                    to='cms.CMSPlugin', primary_key=True)),
                ('body', models.TextField()),
                ('additional_text', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='InvalidSearchFieldsModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(
                    serialize=False, parent_link=True, auto_created=True,
                    to='cms.CMSPlugin', primary_key=True)),
                ('body', models.TextField()),
                ('additional_text', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
