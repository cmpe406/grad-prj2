# Generated by Django 4.0 on 2022-06-16 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0043_alter_course_course_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_views',
            field=models.BigIntegerField(default=0),
        ),
    ]