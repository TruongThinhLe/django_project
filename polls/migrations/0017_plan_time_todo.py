# Generated by Django 3.2.9 on 2022-01-04 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_alter_list_todo_check_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='time_todo',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]