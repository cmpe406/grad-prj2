# Generated by Django 4.0 on 2022-08-08 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0050_teacherstudentchat'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='facebook_url',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='instgram_url',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='twitter_url',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='website_url',
            field=models.URLField(null=True),
        ),
    ]