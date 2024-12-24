from django.db import models

from eleve.models import Eleve

from note.models import Note

from annee_scolaire.models import AnneeScolaire

from django.db.models import Avg, F, Sum

class BulletinTrimestriel(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE)
    trimestre = models.IntegerField(choices=[(1, "1er"), (2, "2ème"), (3, "3ème")])

    @property
    def moyennes_par_matiere(self):
        notes = Note.objects.filter(eleve=self.eleve, annee_scolaire=self.annee_scolaire).values(
            'matiere__nom'
        ).annotate(moyenne_matiere=Avg((F('note_comp') + F('note_cours')) / 2))
        return notes

    @property
    def moyenne_totale(self):
        notes = Note.objects.filter(eleve=self.eleve, annee_scolaire=self.annee_scolaire).annotate(
            moyenne_individuelle=(F('note_comp') + F('note_cours')) / 2
        )
        total_notes = notes.aggregate(Sum('moyenne_individuelle'))['moyenne_individuelle__sum'] or 0
        return total_notes / notes.count() if notes.exists() else 0

    def __str__(self):
        return f"Bulletin {self.eleve} - Trimestre {self.trimestre}"
