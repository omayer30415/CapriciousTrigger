# Generated by Django 3.2.7 on 2021-12-19 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('singlePlayer', '0003_alter_general_commander'),
    ]

    operations = [
        migrations.AddField(
            model_name='soldier',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='soldiers', related_query_name='soldiers', to='singlePlayer.team'),
        ),
    ]
