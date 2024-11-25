# Generated by Django 5.0.9 on 2024-11-25 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0003_project_sync_command'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='label',
            field=models.CharField(default='New Log', max_length=100),
        ),
        migrations.AlterField(
            model_name='project',
            name='sync_command',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]