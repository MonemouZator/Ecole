from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# table administrateurs
class Administrateur(AbstractUser):
     
        TYPE=[
            ('FONDATEUR','Fondateur'),
            ('DG','Directeur'),
            ('CENSSEUR','Censseur'),
            ('COMPTABLE ','Comptable'),
            ('ENSEIGNANT','Enseignant'),
        
        ]
        
        fonction=models.CharField(max_length=256,choices=TYPE,null=True)
        nom=models.CharField(max_length=40,db_index=False)
        prenom=models.CharField(max_length=40,db_index=False)
        specialite=models.CharField(max_length=40,db_index=False)
        telephone=models.CharField(max_length=15,db_index=False)
        genre=models.CharField(max_length=15,db_index=False)
        adresse=models.CharField(max_length=60,db_index=False)
        date_naiss=models.DateField(null=True,blank=True)
        lieu_naiss=models.CharField(max_length=30,db_index=False)
        photo=models.ImageField(null=True,blank=True)
        contact=models.CharField(max_length=128,null=True,blank=True)
        date_naissance=models.DateField(null=True,blank=True)
        filiation=models.TextField(null=True,blank=True)
        def __str__(self):
         return f"@{self.first_name} {self.last_name} {self.telephone}"