# Generated by Django 3.2.7 on 2021-11-10 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newgen', '0005_questions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questions',
            options={'ordering': ['-created_at'], 'verbose_name': 'Вопрос методисту', 'verbose_name_plural': 'Вопросы методисту'},
        ),
        migrations.RemoveField(
            model_name='questions',
            name='slug',
        ),
        migrations.AlterField(
            model_name='questions',
            name='content',
            field=models.TextField(blank=True, verbose_name='Содержание вопроса'),
        ),
    ]
