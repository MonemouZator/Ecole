from django.db import models

from niveau.models import Niveau

from groupe_classe.models import GroupeClasse

from annee_scolaire.models import AnneeScolaire


from django.utils import timezone


from django.db import models
from niveau.models import Niveau
from groupe_classe.models import GroupeClasse
from annee_scolaire.models import AnneeScolaire

class Eleve(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    groupe_classe = models.ForeignKey(GroupeClasse, on_delete=models.CASCADE)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.TextField()
    genre = models.CharField(max_length=15)
    telephone = models.CharField(max_length=15, unique=True)
    photo = models.ImageField(upload_to='eleve/img', null=True, blank=True)
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.SET_NULL, null=True, blank=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.SET_NULL, null=True, blank=True)
    
    pere = models.CharField(max_length=191)
    profession_pere = models.CharField(max_length=191)
    contact_parent = models.CharField(max_length=15, null=True, blank=True)
    mere = models.CharField(max_length=191)
    profession_mere = models.CharField(max_length=191)
    contact_mere = models.CharField(max_length=15, null=True, blank=True)
    
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.niveau and self.annee_scolaire:
            montant_total = self.niveau.montant_frais or 0  # Vérifie si un montant est défini
            tranche1 = montant_total / 2
            tranche2 = montant_total / 2

            frais_existe = FraisScolarite.objects.filter(eleve=self, annee_scolaire=self.annee_scolaire).exists()
            if not frais_existe:
                frais = FraisScolarite.objects.create(
                    eleve=self,
                    annee_scolaire=self.annee_scolaire,
                    tranche1=tranche1,
                    tranche2=tranche2,
                    montant_total=montant_total,
                    total_paye=tranche1,  # Mise à jour du paiement de la première tranche
                    solde=montant_total - tranche1,
                    est_paye_tranche1=True
                )

                Recu.objects.create(
                    frais_scolarite=frais,
                    montant=tranche1,
                    details=f"Premier paiement des frais pour {self.nom} {self.prenom}."
                )


# Assurez-vous d'avoir le modèle Recu défini auparavant pour ce code à fonctionner
class FraisScolarite(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    annee_scolaire =  models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE)
    tranche1 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tranche2 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    est_paye_tranche1 = models.BooleanField(default=False)
    est_paye_tranche2 = models.BooleanField(default=False)

    def __str__(self):
        return f"Frais pour {self.eleve.nom} {self.eleve.prenom}"


    def save(self, *args, **kwargs):
        if self.total_paye >= self.tranche1:
            self.est_paye_tranche1 = True
        if self.total_paye >= (self.tranche1 + self.tranche2):
            self.est_paye_tranche2 = True
        self.solde = self.montant_total - self.total_paye
        super().save(*args, **kwargs)


    def payer_tranche2(self):
        """Paiement de la deuxième tranche"""
        if self.solde > 0 and not self.est_paye_tranche2:
            montant_a_payer = min(self.solde, self.tranche2)
            self.total_paye += montant_a_payer
            self.solde -= montant_a_payer
            self.est_paye_tranche2 = self.total_paye >= self.montant_total  # Vérifie si tout est payé
            self.save()

            Recu.objects.create(
                frais_scolarite=self,
                montant=montant_a_payer,
                details=f"Paiement de la deuxième tranche pour {self.eleve.nom} {self.eleve.prenom}."
            )

    def payer_complet(self):
        """Paiement total des frais scolaires"""
        if self.solde > 0:
            montant_a_payer = self.solde
            self.total_paye += montant_a_payer
            self.solde = 0
            self.est_paye_tranche1 = True
            self.est_paye_tranche2 = True
            self.save()

            Recu.objects.create(
                frais_scolarite=self,
                montant=montant_a_payer,
                details=f"Paiement complet des frais pour {self.eleve.nom} {self.eleve.prenom}."
            )


    
class Recu(models.Model):
    frais_scolarite = models.ForeignKey(FraisScolarite, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_recu = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    def __str__(self):
        return f"Reçu {self.id} - {self.frais_scolarite.eleve.nom} {self.frais_scolarite.eleve.prenom}"
