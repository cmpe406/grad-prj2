# Generated by Django 4.0 on 2022-05-12 05:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_courserating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courserating',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.course'),
        ),
    ]