# Generated by Django 4.2.4 on 2024-12-25 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrateur',
            name='date_naiss',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='administrateur',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]