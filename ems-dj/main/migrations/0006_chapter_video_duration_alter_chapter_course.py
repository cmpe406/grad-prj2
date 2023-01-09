# Generated by Django 4.0 on 2022-03-25 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_student_options_chapter'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='video_duration',
            field=models.CharField(help_text='Save video duration in seconds', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_chapters', to='main.course'),
        ),
    ]