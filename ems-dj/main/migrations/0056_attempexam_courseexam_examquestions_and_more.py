# Generated by Django 4.1.5 on 2023-01-09 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0055_alter_attempquiz_options_alter_course_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttempExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('right_ans', models.CharField(max_length=200, null=True)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '12. Attempted Questions',
            },
        ),
        migrations.CreateModel(
            name='CourseExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '11. Course Exam',
            },
        ),
        migrations.CreateModel(
            name='ExamQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions', models.CharField(max_length=200)),
                ('ans1', models.CharField(max_length=200)),
                ('ans2', models.CharField(max_length=200)),
                ('ans3', models.CharField(max_length=200)),
                ('ans4', models.CharField(max_length=200)),
                ('right_ans', models.CharField(max_length=200)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '10. Exam Questions',
            },
        ),
        migrations.RemoveField(
            model_name='coursequiz',
            name='course',
        ),
        migrations.RemoveField(
            model_name='coursequiz',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='coursequiz',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='quizquestions',
            name='quiz',
        ),
        migrations.AlterModelOptions(
            name='exam',
            options={'verbose_name_plural': '8. Exam'},
        ),
        migrations.RenameModel(
            old_name='Quiz',
            new_name='Exam',
        ),
        migrations.DeleteModel(
            name='AttempQuiz',
        ),
        migrations.DeleteModel(
            name='CourseQuiz',
        ),
        migrations.DeleteModel(
            name='QuizQuestions',
        ),
        migrations.AddField(
            model_name='examquestions',
            name='Exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.exam'),
        ),
        migrations.AddField(
            model_name='courseexam',
            name='Exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.exam'),
        ),
        migrations.AddField(
            model_name='courseexam',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.course'),
        ),
        migrations.AddField(
            model_name='courseexam',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.teacher'),
        ),
        migrations.AddField(
            model_name='attempexam',
            name='Exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.exam'),
        ),
        migrations.AddField(
            model_name='attempexam',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.examquestions'),
        ),
        migrations.AddField(
            model_name='attempexam',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.student'),
        ),
    ]
