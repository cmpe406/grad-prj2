# Generated by Django 4.0 on 2022-07-22 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0048_student_otp_digit_student_verify_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='login_via_otp',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='teacher',
            name='login_via_otp',
            field=models.BooleanField(default=False),
        ),
    ]
