# Generated by Django 4.0.4 on 2022-05-18 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0006_todolist_session_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='is_late',
            field=models.BooleanField(default=False),
        ),
    ]
