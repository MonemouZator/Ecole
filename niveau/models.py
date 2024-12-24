from django.db import models

from cycle.models import Cycle

# Niveau
class Niveau(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)  # Nouveau lien avec le Cycle
    nom = models.CharField(max_length=50,db_index=False)  # Exemple : "CP", "6ème", "Terminale"

    def __str__(self):
        return f"{self.cycle.nom} - {self.nom}"
