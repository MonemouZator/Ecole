from django.db import models

from niveau.models import Niveau

from groupe_classe.models import GroupeClasse

from annee_scolaire.models import AnneeScolaire


from django.utils import timezone



class Eleve(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    groupe_classe = models.ForeignKey(GroupeClasse, on_delete=models.CASCADE)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.TextField()
    genre = models.CharField(max_length=15)
    telephone = models.CharField(max_length=15, db_index=False, unique=True)
    photo = models.ImageField(upload_to='eleve/img', null=True, blank=True)
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.SET_NULL, null=True, blank=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.SET_NULL, null=True, blank=True)

    pere = models.CharField(max_length=191, db_index=False)
    profession_pere = models.CharField(max_length=191, db_index=False)
    contact_parent = models.CharField(max_length=15, null=True, blank=True, db_index=False)
    mere = models.CharField(max_length=191, db_index=False)
    profession_mere = models.CharField(max_length=191, db_index=False)
    contact_mere = models.CharField(max_length=15, null=True, blank=True, db_index=False)

    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"

    def save(self, *args, **kwargs):
        # Enregistrement de l'élève
        super().save(*args, **kwargs)

        # Vérifier si les frais de scolarité existent déjà
        frais_existe = FraisScolarite.objects.filter(eleve=self, annee_scolaire=self.annee_scolaire).exists()
        if not frais_existe:
            # Calcul des frais de scolarité et première tranche
            montant_total = self.niveau.montant_frais  # Montant total des frais pour ce niveau
            tranche1 = montant_total / 2  # Première tranche (50% du montant total)
            tranche2 = montant_total / 2  # Deuxième tranche (50% du montant total)
            solde = montant_total - tranche1  # Solde restant après paiement de la première tranche

            # Créer l'enregistrement des frais de scolarité
            frais = FraisScolarite.objects.create(
                eleve=self,
                annee_scolaire=self.annee_scolaire.nom,
                tranche1=tranche1,
                tranche2=tranche2,
                montant_total=montant_total,
                solde=solde
            )

            # Créer le reçu pour la première tranche
            Recu.objects.create(
                frais_scolarite=frais,
                montant=tranche1,
                details=f"Premier paiement de la première tranche des frais pour l'élève {self.nom} {self.prenom}"
            )



from django.db import models

# Assurez-vous d'avoir le modèle Recu défini auparavant pour ce code à fonctionner
class FraisScolarite(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    annee_scolaire = models.CharField(max_length=9)
    tranche1 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tranche2 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    est_paye_tranche2 = models.BooleanField(default=False)  # Ajout du champ pour suivre le paiement de la tranche 2

    def __str__(self):
        return f"Frais pour {self.eleve.nom} {self.eleve.prenom}"

    def payer_tranche2(self):
        """Payer la deuxième tranche des frais de scolarité."""
        if self.solde > 0 and not self.est_paye_tranche2:  # Vérifie si la deuxième tranche n'a pas déjà été payée
            montant_a_payer = self.tranche2 if self.solde >= self.tranche2 else self.solde  # Si solde insuffisant, on paie le solde restant
            self.total_paye += montant_a_payer
            self.solde -= montant_a_payer  # Mise à jour du solde
            self.est_paye_tranche2 = True if self.solde == 0 else False  # Si tout est payé, on marque comme payé
            self.save()

            # Créer un reçu pour la deuxième tranche
            Recu.objects.create(
                frais_scolarite=self,
                montant=montant_a_payer,
                details=f"Deuxième paiement des frais de scolarité pour {self.eleve.nom} {self.eleve.prenom}."
            )

    def payer_complet(self):
        """Payer la totalité des frais de scolarité, y compris la deuxième tranche."""
        if self.solde > 0:  # Vérifie s'il reste un solde à payer
            montant_a_payer = self.solde  # Montant restant à payer
            self.total_paye += montant_a_payer
            self.solde = 0  # Le solde devient zéro, paiement complet
            self.est_paye_tranche2 = True  # Marque que la deuxième tranche est payée
            self.save()

            # Créer un reçu pour le paiement complet
            Recu.objects.create(
                frais_scolarite=self,
                montant=montant_a_payer,
                details=f"Paiement complet des frais de scolarité pour {self.eleve.nom} {self.eleve.prenom}."
            )


class Recu(models.Model):
    frais_scolarite = models.ForeignKey(FraisScolarite, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_recu = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    def __str__(self):
        return f"Reçu {self.id} - {self.frais_scolarite.eleve.nom} {self.frais_scolarite.eleve.prenom}"
