from django.db import models

# Année Scolaire
class AnneeScolaire(models.Model):
    nom = models.CharField(max_length=9,db_index=False)  # Exemple : "2023-2024"
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return self.nom