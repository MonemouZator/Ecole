from django.db import models
from niveau.models import Niveau
from groupe_classe.models import GroupeClasse
from annee_scolaire.models import AnneeScolaire

# Élève
class Eleve(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    groupe_classe = models.ForeignKey(GroupeClasse, on_delete=models.CASCADE)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.TextField()
    genre = models.CharField(max_length=15)
    telephone = models.CharField(max_length=15, db_index=False, unique=True)  # Téléphone unique
    photo = models.ImageField(upload_to='eleve/img', null=True, blank=True)  # Ajouter un upload_to pour les photos
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.SET_NULL, null=True, blank=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.SET_NULL, null=True, blank=True)
    
    pere = models.CharField(max_length=191, db_index=False)
    profession_pere = models.CharField(max_length=191, db_index=False)
    contact_parent = models.CharField(max_length=15, null=True, blank=True, db_index=False)
    mere = models.CharField(max_length=191, db_index=False)
    profession_mere = models.CharField(max_length=191, db_index=False)
    contact_mere = models.CharField(max_length=15, null=True, blank=True, db_index=False)
    
    # Nouveau champ booléen pour savoir si l'élève est actif
    actif = models.BooleanField(default=True)  # Indiquer si l'élève est toujours inscrit ou actif

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    # Optionnel : Méthode pour obtenir un nom complet
    def get_full_name(self):
        return f"{self.prenom} {self.nom}"
