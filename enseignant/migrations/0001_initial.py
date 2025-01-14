# Generated by Django 4.2.4 on 2025-01-05 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enseignant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=40, unique=True)),
                ('prenom', models.CharField(max_length=40)),
                ('specialite', models.CharField(max_length=40)),
                ('telephone', models.CharField(max_length=15)),
                ('Sexe', models.CharField(choices=[('H', 'Masculin'), ('F', 'Feminin')], max_length=10)),
                ('adresse', models.CharField(max_length=60)),
                ('date_naiss', models.DateField()),
                ('lieu_naiss', models.CharField(max_length=30)),
                ('photo', models.ImageField(upload_to='')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
