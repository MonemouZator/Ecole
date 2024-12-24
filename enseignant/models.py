from django.db import models
from matiere.models import Matiere


class Enseignant(models.Model):
    nom = models.CharField(max_length=50,db_index=False)
    prenom = models.CharField(max_length=50,db_index=False)
    specialite = models.CharField(max_length=50,db_index=False)
    email = models.EmailField( max_length=254)  # Limitation explicite
    telephone = models.CharField(max_length=15, blank=True, null=True,db_index=False)

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.specialite}"
