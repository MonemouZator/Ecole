from django.db import models

from eleve.models import Eleve

from matiere.models import Matiere

from annee_scolaire.models import AnneeScolaire

class Note(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    note_comp = models.FloatField()  # Note de compétence
    note_cours = models.FloatField()  # Note de cours
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE)

    @property
    def moyenne(self):
        """Calcule la moyenne des deux notes."""
        return (self.note_comp + self.note_cours) / 2

    def __str__(self):
        return f"{self.eleve} - {self.matiere} : Moyenne {self.moyenne:.2f}"
