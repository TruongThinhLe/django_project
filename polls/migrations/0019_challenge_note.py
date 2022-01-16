# Generated by Django 3.2.9 on 2022-01-15 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0018_auto_20220104_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Challenge', models.TextField()),
                ('Time_pub', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Note', models.TextField(max_length=50)),
                ('Time_pub', models.DateField(auto_now_add=True)),
                ('Detail', models.TextField(max_length=100)),
            ],
        ),
    ]
