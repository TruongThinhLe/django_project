# Generated by Django 3.2.9 on 2022-01-16 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0019_challenge_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='Status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='Challenge',
            field=models.TextField(max_length=50),
        ),
    ]