# Generated by Django 3.2.7 on 2021-12-21 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('singlePlayer', '0007_auto_20211220_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_score', models.IntegerField()),
                ('opponent_score', models.IntegerField()),
            ],
        ),
    ]
