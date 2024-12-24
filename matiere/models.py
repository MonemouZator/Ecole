from django.db import models
from niveau.models import Niveau

# Matière
class Matiere(models.Model):
    nom = models.CharField(max_length=50,db_index=False)
    coefficient = models.FloatField()
    niveau = models.ManyToManyField(Niveau)

    def __str__(self):
        return self.nom
