from django.shortcuts import render,redirect,get_object_or_404
from enseignant.models import Enseignant
def maitre(request):
        
        enseignants=Enseignant.objects.all()

        context={
                    "enseignants":enseignants
                }
        return render(request, 'base/pages/tables/data.html',context)

# FONCTION D'ENREGISTREMENT DES ENSEIGNANTS

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
    
    #FONCTION DE MODIFICATION DES INFORMATIONS

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
    
    #FONCTION DE SUPPRESSION DES INFORMATIONS

def  supprim(request,pk):
    enseignant=get_object_or_404(Enseignant,id=pk)
    enseignant.delete()

    return redirect('enseignant')

def detail_enseignant(request):
     
     return render(request,'enseignant/enseignant.html')

#PAIEMENT DES SALAIRES
from django.shortcuts import render, redirect
from .models import PaiementSalaire, Depense, Enseignant
from django.utils import timezone

# Payer un enseignant (sans ModelForm)
def paiement_salaire(request):
    enseignants = Enseignant.objects.all()  # Récupérer tous les enseignants
    paiements = PaiementSalaire.objects.all()  # Récupérer tous les paiements

    if request.method == 'POST':
        enseignant_id = request.POST.get('enseignant')
        montant = request.POST.get('montant')
        date_paiement = request.POST.get('date_paiement')
        statut = request.POST.get('statut')

        # Vérification que tous les champs sont fournis
        if enseignant_id and montant and date_paiement:
            try:
                enseignant = Enseignant.objects.get(id=enseignant_id)  # Récupérer l'enseignant
                # Ajouter le paiement si l'enseignant existe
                PaiementSalaire.objects.create(
                    enseignant=enseignant,
                    montant=montant,
                    date_paiement=date_paiement,
                    statut=statut,
                )
                messages.success(request, "Paiement effectué avec succès.")
                # Rediriger pour éviter la soumission répétée lors de l'actualisation
                return redirect('paiement_salaire')  # Remplacez par l'URL ou le nom de la vue approprié

            except Enseignant.DoesNotExist:
                messages.error(request, "L'enseignant sélectionné n'existe pas.")
        else:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")

    return render(request, 'enseignant/paiement_salaire.html', {
        'enseignants': enseignants,
        'paiements': paiements,
    })


# Ajouter une dépense (sans ModelForm)
from django.shortcuts import render, redirect
from django.contrib import messages  # Pour afficher des messages
from .models import Depense

# views.py
from django.contrib import messages

from django.shortcuts import render, redirect
from .models import Depense
from django.contrib import messages

def ajouter_depense(request):
    if request.method == "POST":
        description = request.POST.get("description")
        montant = request.POST.get("montant")
        date_depense = request.POST.get("date_depense")

        if description and montant and date_depense:
            # Créer une nouvelle dépense
            Depense.objects.create(
                description=description,
                montant=montant,
                date_depense=date_depense
            )
            messages.success(request, "Dépense ajoutée avec succès !")
            # Après avoir ajouté la dépense, rediriger pour éviter le renvoi du formulaire
            return redirect('depense')  # Redirection vers la même vue 'depense'

    # Récupérer les dépenses déjà enregistrées
    depenses = Depense.objects.all()
    return render(request, 'enseignant/depense.html', {'depenses': depenses})


   
# Liste des paiements
def liste_paiements(request):
    paiements = PaiementSalaire.objects.all()
    return render(request, 'enseignant/liste_paiements.html', {'paiements': paiements})

# Liste des dépenses
def liste_depenses(request):
    depenses = Depense.objects.all()
    return render(request, 'enseignant/liste_depenses.html', {'depenses': depenses})


from django.shortcuts import render
from eleve .models import Eleve, FraisScolarite

def bilan_financier(request):
    # Calcul des entrées : somme des frais de scolarité des élèves
    total_entrees = 0
    for eleve in Eleve.objects.all():
        # Accéder à l'objet FraisScolarite lié à l'élève
        frais_scolarite = FraisScolarite.objects.filter(eleve=eleve).first()
        if frais_scolarite:
            total_entrees += frais_scolarite.montant_total

    # Calcul des sorties :
    # Total des dépenses
    total_depenses = sum(depense.montant for depense in Depense.objects.all())
    
    # Total des paiements de salaires
    total_salaires = sum(paiement.montant for paiement in PaiementSalaire.objects.all())

    # Total des sorties = total des dépenses + total des paiements de salaires
    total_sorties = total_depenses + total_salaires

    # Calcul du solde : Entrées - Sorties
    solde = total_entrees - total_sorties

    context = {
        'total_entrees': total_entrees,
        'total_depenses': total_depenses,
        'total_salaires': total_salaires,
        'total_sorties': total_sorties,
        'solde': solde,
    }

    return render(request, 'enseignant/bilan_financier.html', context)