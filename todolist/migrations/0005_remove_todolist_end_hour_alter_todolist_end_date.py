# Generated by Django 4.0.4 on 2022-05-14 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0004_alter_todolist_end_date_alter_todolist_end_hour'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todolist',
            name='end_hour',
        ),
        migrations.AlterField(
            model_name='todolist',
            name='end_date',
            field=models.DateTimeField(blank=True),
        ),
    ]