# Generated by Django 5.0.9 on 2024-11-25 22:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0005_logentry_level_logentry_summary_logentry_timestamp_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logentry',
            name='content',
        ),
    ]