# Generated by Django 3.2.9 on 2022-01-20 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0021_plan_period_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='Period_re',
            field=models.IntegerField(default=3),
        ),
    ]