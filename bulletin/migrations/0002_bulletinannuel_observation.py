# Generated by Django 4.2.4 on 2025-02-10 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bulletinannuel',
            name='observation',
            field=models.TextField(blank=True, null=True),
        ),
    ]
