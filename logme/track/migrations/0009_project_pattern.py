# Generated by Django 5.0.9 on 2024-12-05 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0008_alter_logentry_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='pattern',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]