from django.db import models
from cycle.models import Cycle

# Niveau
class Niveau(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)  # Nouveau lien avec le Cycle
    nom = models.CharField(max_length=50, unique=True)  # Exemple : "CP", "6ème", "Terminale"

    class Meta:
        unique_together = ('cycle', 'nom')  # Empêcher les doublons du même niveau dans un cycle

    def __str__(self):
        return f"{self.nom} "  # Affichage plus détaillé (Nom du niveau + cycle)
