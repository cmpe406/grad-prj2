# Generated by Django 4.0 on 2022-03-26 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_chapter_video_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='video_duration',
            field=models.PositiveBigIntegerField(null=True),
        ),
    ]
