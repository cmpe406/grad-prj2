# Generated by Django 4.0 on 2022-08-08 01:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0051_teacher_facebook_url_teacher_instgram_url_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='instgram_url',
            new_name='instagram_url',
        ),
    ]