# Generated by Django 3.2.7 on 2021-10-28 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_alter_english_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='english',
            name='example',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='english',
            name='meaning',
            field=models.TextField(max_length=50, null=True),
        ),
    ]
