# Generated by Django 4.0 on 2022-03-26 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_chapter_video_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='video_duration',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
