# Generated by Django 5.0.9 on 2024-11-25 19:00

import django_extensions.db.fields
import logme.track.fields
from django.db import migrations, models

def create_default_log_levels(apps, schema_editor):
    LogLevel = apps.get_model('track', 'LogLevel')
    default_levels = [
        {'title': 'DEBUG', 'color_hex': '#636363'},
        {'title': 'INFO', 'color_hex': '#2563EB'},
        {'title': 'WARNING', 'color_hex': '#F59E0B'},
        {'title': 'ERROR', 'color_hex': '#DC2626'},
        {'title': 'EMERGENCY', 'color_hex': '#FF0000'},
    ]

    for level in default_levels:
        LogLevel.objects.create(**level)

def reverse_default_log_levels(apps, schema_editor):
    LogLevel = apps.get_model('track', 'LogLevel')
    LogLevel.objects.filter(title__in=['DEBUG', 'INFO', 'WARNING', 'ERROR']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('track', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['title'])),
                ('color_hex', logme.track.fields.HexColorField(default='COCOCO', max_length=7)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='levels',
            field=models.ManyToManyField(related_name='projects', to='track.loglevel'),
        ),
        migrations.RunPython(
            create_default_log_levels,
            reverse_default_log_levels
        ),
    ]
