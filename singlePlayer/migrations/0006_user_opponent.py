# Generated by Django 3.2.7 on 2021-12-19 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('singlePlayer', '0005_alter_soldier_commander'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='opponent',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opponent', to='singlePlayer.team'),
        ),
    ]
