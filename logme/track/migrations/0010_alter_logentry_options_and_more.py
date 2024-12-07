# Generated by Django 5.0.9 on 2024-12-07 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0009_project_pattern'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logentry',
            options={'get_latest_by': 'modified'},
        ),
        migrations.RemoveConstraint(
            model_name='logentry',
            name='unique_summary_timestamp',
        ),
    ]
