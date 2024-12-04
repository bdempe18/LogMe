# Generated by Django 5.0.9 on 2024-11-25 22:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0004_alter_logentry_label_alter_project_sync_command'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='level',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='track.loglevel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='logentry',
            name='summary',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='logentry',
            name='timestamp',
            field=models.DateTimeField(default='2024-02-02 00:00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='logentry',
            name='trace',
            field=models.TextField(blank=True),
        ),
    ]
