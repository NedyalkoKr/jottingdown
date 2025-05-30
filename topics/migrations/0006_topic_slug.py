# Generated by Django 5.2 on 2025-04-22 11:45

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0005_topic_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, editable=False, null=True, populate_from='topic_id'),
        ),
    ]
