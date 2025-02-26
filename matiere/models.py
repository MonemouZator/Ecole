from django.db import models
from niveau.models import Niveau
#from enseignant.models import Enseignant
# Matière
class Matiere(models.Model):
    nom = models.CharField(max_length=50,db_index=False ,unique=True)
    coefficient = models.FloatField()
    niveau = models.ForeignKey(Niveau,on_delete=models.CASCADE)
    #enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nom}"
 