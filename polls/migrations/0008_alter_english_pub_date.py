# Generated by Django 3.2.7 on 2021-10-27 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20211027_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='english',
            name='pub_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
