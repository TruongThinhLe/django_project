# Generated by Django 3.2.7 on 2021-10-19 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_plan_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='status',
            field=models.IntegerField(null=True),
        ),
    ]
