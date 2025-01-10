from django.db import models
from matiere.models import Matiere


class Enseignant(models.Model):
        

        Sexe=[
        ("H","Masculin"),
        ("F","Feminin"),
    ]
        nom=models.CharField(max_length=40,db_index=False ,unique=True)
        prenom=models.CharField(max_length=40,db_index=False)
        specialite=models.CharField(max_length=40,db_index=False)
        telephone=models.CharField(max_length=15,db_index=False)
        Sexe=models.CharField(max_length=10,choices=Sexe,db_index=False)
        adresse=models.CharField(max_length=60,db_index=False)
        date_naiss=models.DateField()
        lieu_naiss=models.CharField(max_length=30,db_index=False)
        photo=models.ImageField()
        email = models.EmailField( max_length=254)  # Limitation explicite
        def __str__(self) -> str:
            return f"{self.nom}{self.prenom}{self.telephone}"




    
    