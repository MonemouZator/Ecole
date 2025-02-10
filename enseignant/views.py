from django.shortcuts import render,redirect,get_object_or_404
from enseignant.models import Enseignant,PaiementSalaire
from django.shortcuts import render, redirect
from .models import Depense
from django.contrib import messages

from eleve .models import Eleve , FraisScolarite
from annee_scolaire.models import AnneeScolaire
from django.db.models import Sum
from django.db import models  # Importation de models





##################### LISTE DES ENSEIGNANTS ###################################

def maitre(request):
        
        enseignants=Enseignant.objects.all()

        context={
                    "enseignants":enseignants
                }
        return render(request, 'base/pages/tables/data.html',context)


################## FONCTION D'ENREGISTREMENT DES ENSEIGNANTS ####################

def ajout(request):
    if request.method=="POST": 
           
            nom=request.POST.get('nom')
            prenom=request.POST.get('prenom')
            tel=request.POST.get('tel')
            sexe=request.POST.get('sexe')
            adresse=request.POST.get('adresse')
            date=request.POST.get('naissance')
            lieu=request.POST.get('lieu')
            photo=request.POST.get('photo')
            specilite=request.POST.get('sp')
            email=request.POST.get('email')
            ensi=Enseignant.objects.create(
                nom=nom,
                prenom=prenom,
                telephone=tel,
                Sexe=sexe,
                adresse=adresse,
                date_naiss=date,
                lieu_naiss=lieu,
                photo=photo,
                specialite=specilite,
                email=email,
            )
            ensi.save()

            return redirect('enseignant')
    else:
        return redirect('enseignant')


    
####################### FONCTION DE MODIFICATION DES INFORMATIONS ######################

def modifier(request):
    if request.method=='POST':
        pk=request.POST.get('id')
        maitre=get_object_or_404(Enseignant,id=pk)
        nom=request.POST.get('nom')
        prenom=request.POST.get('prenom')
        tel=request.POST.get('tel')
        sexe=request.POST.get('sexe')
        adresse=request.POST.get('adresse')
        date=request.POST.get('naissance')
        lieu=request.POST.get('lieu')
        photo=request.POST.get('photo')
        specilite=request.POST.get('sp')
        email=request.POST.get('email')

        maitre.nom=nom
        maitre.prenom=prenom
        maitre.telephone=tel
        maitre.sexe=sexe
        maitre.adresse=adresse
        maitre.date_naissance=date
        maitre.lieu_naiss=lieu
        maitre.photo=photo
        maitre.specialite=specilite
        maitre.email=email
        maitre.save()

        return redirect('enseignant')
    else:
        return redirect('enseignant')

    
##################FONCTION DE SUPPRESSION DES INFORMATIONS#####################

def  supprim(request,pk):
    enseignant=get_object_or_404(Enseignant,id=pk)
    enseignant.delete()

    return redirect('enseignant')

def detail_enseignant(request):
     
     return render(request,'enseignant/enseignant.html')



#########################PAIEMENT DES SALAIRES#################################

def paiement_salaire(request):
    enseignants = Enseignant.objects.all()  # Récupérer tous les enseignants
    paiements = PaiementSalaire.objects.all()  # Récupérer tous les paiements
    annees_scolaires = AnneeScolaire.objects.all()  # Récupérer toutes les années scolaires

    if request.method == 'POST':
        enseignant_id = request.POST.get('enseignant')
        montant = request.POST.get('montant')
        date_paiement = request.POST.get('date_paiement')
        statut = request.POST.get('statut')
        annee_scolaire_id = request.POST.get('annee_scolaire')

        # Vérification que tous les champs sont fournis
        if enseignant_id and montant and date_paiement and annee_scolaire_id:
            try:
                enseignant = Enseignant.objects.get(id=enseignant_id)  # Récupérer l'enseignant
                annee_scolaire = AnneeScolaire.objects.get(id=annee_scolaire_id)  # Récupérer l'année scolaire

                # Calcul des entrées et sorties pour l'année scolaire
                total_entrées = FraisScolarite.objects.filter(annee_scolaire=annee_scolaire).aggregate(total=models.Sum('montant_total'))['total'] or 0
                total_sorties_salaire = PaiementSalaire.objects.filter(annee_scolaire=annee_scolaire).aggregate(total=models.Sum('montant'))['total'] or 0
                total_sorties_depense = Depense.objects.filter(annee_scolaire=annee_scolaire).aggregate(total=models.Sum('montant'))['total'] or 0
                total_sorties = total_sorties_salaire + total_sorties_depense
                solde = total_entrées - total_sorties

                # Vérification du solde avant de procéder à l'enregistrement
                if solde <= 0:
                    messages.error(request, "Le solde est insuffisant pour enregistrer ce paiement.")
                    return redirect('paiement_salaire')  # Remplacez par l'URL ou le nom de la vue approprié

                # Ajouter le paiement si le solde est suffisant
                PaiementSalaire.objects.create(
                    enseignant=enseignant,
                    montant=montant,
                    date_paiement=date_paiement,
                    statut=statut,
                    annee_scolaire=annee_scolaire,
                )
                messages.success(request, "Paiement effectué avec succès.")
                return redirect('paiement_salaire')

            except Enseignant.DoesNotExist:
                messages.error(request, "L'enseignant sélectionné n'existe pas.")
            except AnneeScolaire.DoesNotExist:
                messages.error(request, "L'année scolaire sélectionnée n'existe pas.")
        else:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")

    return render(request, 'enseignant/paiement_salaire.html', {
        'enseignants': enseignants,
        'paiements': paiements,
        'annees_scolaires': annees_scolaires,
    })



################ Ajouter une dépense (sans ModelForm)#############################



def ajouter_depense(request):
    annees_scolaires = AnneeScolaire.objects.all()  # Récupérer toutes les années scolaires
    depenses = Depense.objects.all()  # Récupérer toutes les dépenses pour les afficher

    if request.method == 'POST':
        montant = request.POST.get('montant')
        description = request.POST.get('description')
        annee_scolaire_id = request.POST.get('annee_scolaire')

        if montant and description and annee_scolaire_id:
            try:
                annee_scolaire = AnneeScolaire.objects.get(id=annee_scolaire_id)  # Récupérer l'année scolaire

                # Calcul des entrées et sorties pour l'année scolaire
                total_entrées = FraisScolarite.objects.filter(annee_scolaire=annee_scolaire).aggregate(total=models.Sum('montant_total'))['total'] or 0
                total_sorties_salaire = PaiementSalaire.objects.filter(annee_scolaire=annee_scolaire).aggregate(total=models.Sum('montant'))['total'] or 0
                total_sorties_depense = Depense.objects.filter(annee_scolaire=annee_scolaire).aggregate(total=models.Sum('montant'))['total'] or 0
                total_sorties = total_sorties_salaire + total_sorties_depense
                solde = total_entrées - total_sorties

                # Afficher les valeurs pour le débogage
                print(f"Total Entrées: {total_entrées}")
                print(f"Total Sorties Salaire: {total_sorties_salaire}")
                print(f"Total Sorties Dépense: {total_sorties_depense}")
                print(f"Solde: {solde}")

                # Vérification du solde avant d'enregistrer la dépense
                if solde <= 0:
                    messages.error(request, "Le solde est insuffisant pour enregistrer cette dépense.")
                    return redirect('depense')

                # Ajouter la dépense si le solde est suffisant
                Depense.objects.create(
                    montant=montant,
                    description=description,
                    annee_scolaire=annee_scolaire,
                )
                messages.success(request, "Dépense enregistrée avec succès.")
                return redirect('depense')

            except AnneeScolaire.DoesNotExist:
                messages.error(request, "L'année scolaire sélectionnée n'existe pas.")
        else:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")

    return render(request, 'enseignant/depense.html', {
        'annees_scolaires': annees_scolaires,
        'depenses': depenses,  # Assurez-vous de passer les dépenses au template
    })



##############################LE BILAN FINANCIER ###################################


def bilan_financier(request):
    # Récupérer toutes les années scolaires disponibles
    annees_scolaires = AnneeScolaire.objects.all()

    # Initialiser les variables de contexte
    total_entrées = 0
    total_sorties = 0
    solde = 0

    # Récupérer l'année scolaire sélectionnée par l'utilisateur, si disponible
    annee_scolaire = None
    selected_annee_id = None
    if 'annee_scolaire' in request.GET:
        selected_annee_id = request.GET['annee_scolaire']
        annee_scolaire = AnneeScolaire.objects.filter(id=selected_annee_id).first()

        if annee_scolaire:
            # Calculer les entrées (frais scolaires payés)
            frais_scolaires = FraisScolarite.objects.filter(annee_scolaire=annee_scolaire)
            total_entrées = sum(frais.total_paye for frais in frais_scolaires)  # Utiliser total_paye

            # Calculer les sorties (salaires et dépenses)
            salaires = PaiementSalaire.objects.filter(annee_scolaire=annee_scolaire)
            depenses = Depense.objects.filter(annee_scolaire=annee_scolaire)

            total_sorties = sum(salaire.montant for salaire in salaires) + sum(depense.montant for depense in depenses)

            # Calculer le solde net
            solde = total_entrées - total_sorties
        else:
            messages.error(request, "L'année scolaire sélectionnée n'est pas valide.")

    context = {
        'annees_scolaires': annees_scolaires,
        'selected_annee_id': selected_annee_id,
        'total_entrées': total_entrées,
        'total_sorties': total_sorties,
        'solde': solde,
        'annee_scolaire': annee_scolaire,
    }

    return render(request, 'enseignant/bilan_financier.html', context)