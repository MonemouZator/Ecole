from django.db import models
from django.contrib.auth.models import AbstractUser

class Administrateur(AbstractUser):
    TYPE = [
        ('FONDATEUR', 'Fondateur'),
        ('DG', 'Directeur'),
        ('CENSEUR', 'Censeur'),
        ('COMPTABLE', 'Administrateur de la Finance'),
        ('ENSEIGNANT', "Administrateur des notes d'élève"),
    ]
    
    
    nom = models.CharField(max_length=40, db_index=True)  # Indexé pour de meilleures performances
    prenom = models.CharField(max_length=40, db_index=True)
    telephone = models.CharField(max_length=15, db_index=True, unique=True)  # Unicité recommandée
    genre = models.CharField(max_length=15)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naiss = models.CharField(max_length=30, db_index=True)
    fonction = models.CharField(max_length=256, choices=TYPE, null=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)  # Dossier de stockage
    email = models.EmailField(max_length=191, unique=True)


    USERNAME_FIELD = 'email'  # On utilise email comme identifiant au lieu de username
    REQUIRED_FIELDS = ['username', 'nom', 'prenom', 'telephone', 'fonction']  # Champs obligatoires pour createsuperuser

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.fonction}"
