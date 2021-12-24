# Generated by Django 3.2.7 on 2021-12-18 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('singlePlayer', '0002_alter_user_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='general',
            name='commander',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='generals', to=settings.AUTH_USER_MODEL),
        ),
    ]