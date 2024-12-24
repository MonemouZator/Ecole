from django.db import models
from niveau.models import Niveau
from groupe_classe.models import GroupeClasse

# Élève
class Eleve(models.Model):
    nom = models.CharField(max_length=50,db_index=False)
    prenom = models.CharField(max_length=50,db_index=False)
    date_naissance = models.DateField()
    adresse = models.TextField()
    telephone = models.CharField(max_length=15,db_index=False)
    # email = models.EmailField(max_length=254)  # Limite explicite
    niveau = models.ForeignKey(Niveau, on_delete=models.SET_NULL, null=True, blank=True)
    groupe_classe = models.ForeignKey(GroupeClasse, on_delete=models.SET_NULL, null=True, blank=True)
    Filiation=models.CharField(max_length=191,db_index=False)
    Contact_parent=models.CharField(max_length=15,null=True,blank=True,db_index=False)

    def __str__(self):
        return f"{self.prenom} {self.nom}{self.Contact_parent}"
