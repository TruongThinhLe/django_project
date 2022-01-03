# Generated by Django 3.2.9 on 2021-12-20 02:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_list_todo_week_todo'),
    ]

    operations = [
        migrations.AddField(
            model_name='week_todo',
            name='Day_todo',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='week_todo',
            name='List',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.list_todo'),
        ),
    ]
