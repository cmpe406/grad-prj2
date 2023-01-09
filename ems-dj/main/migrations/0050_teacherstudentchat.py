# Generated by Django 4.0 on 2022-07-29 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0049_student_login_via_otp_teacher_login_via_otp'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherStudentChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_text', models.TextField()),
                ('msg_from', models.CharField(max_length=100)),
                ('msg_time', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.teacher')),
            ],
            options={
                'verbose_name_plural': '18. Teacher Student Messages',
            },
        ),
    ]
