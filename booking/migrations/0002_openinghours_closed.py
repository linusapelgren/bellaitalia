# Generated by Django 5.1 on 2024-09-02 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='openinghours',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]