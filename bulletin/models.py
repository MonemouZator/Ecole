from django.db import models
from eleve.models import Eleve
from annee_scolaire.models import AnneeScolaire
from note.models import Note
from django.db.models import Avg, F,When,Case

class BulletinTrimestriel(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    trimestre = models.PositiveIntegerField()
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE)

    @property
    def notes_par_matiere(self):
        # Calcul des moyennes des matières pour le trimestre sélectionné
        notes = Note.objects.filter(
            eleve=self.eleve,
            trimestre=self.trimestre,
            annee_scolaire=self.annee_scolaire
        ).values('matiere__nom').annotate(
            moyenne_matiere=Avg(F('note_cours') + F('note_comp')) / 2
        )
        return notes

    @property
    def moyenne_totale(self):
        # Calcul de la moyenne totale du trimestre
        notes = Note.objects.filter(
            eleve=self.eleve,
            trimestre=self.trimestre,
            annee_scolaire=self.annee_scolaire
        )
        moyenne_totale = notes.aggregate(
            moyenne_semestre=Avg(F('note_cours') + F('note_comp')) / 2
        )['moyenne_semestre']
        return round(moyenne_totale, 2) if moyenne_totale else None

    def __str__(self):
        return f"Bulletin Trimestriel - {self.eleve.nom} - Trimestre {self.trimestre}"
    


class BulletinAnnuel(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE)

    @property
    def moyenne_totale_par_trimestre(self):
        # Calcul des moyennes pour les deux trimestres
        moyenne_t1 = Note.objects.filter(
            eleve=self.eleve,
            annee_scolaire=self.annee_scolaire,
            trimestre=1
        ).aggregate(moyenne_t1=Avg(F('note_cours') + F('note_comp')))['moyenne_t1'] or 0

        moyenne_t2 = Note.objects.filter(
            eleve=self.eleve,
            annee_scolaire=self.annee_scolaire,
            trimestre=2
        ).aggregate(moyenne_t2=Avg(F('note_cours') + F('note_comp')))['moyenne_t2'] or 0

        return {
            'moyenne_t1': round(moyenne_t1 / 2, 2),
            'moyenne_t2': round(moyenne_t2 / 2, 2),
        }

    @property
    def moyenne_totale_annuelle(self):
        # Calcul de la moyenne annuelle en fonction des deux trimestres
        moyennes = self.moyenne_totale_par_trimestre
        total_moyennes = moyennes['moyenne_t1'] + moyennes['moyenne_t2']
        return round(total_moyennes / 2, 2)
