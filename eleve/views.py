from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from niveau.models import Niveau
from groupe_classe.models import GroupeClasse
from annee_scolaire.models import AnneeScolaire
from eleve.models import Eleve,Recu,FraisScolarite
# Create your views here.
def eleve(request):

    niveaus=Niveau.objects.all()
    groupes=GroupeClasse.objects.all()
    annes=AnneeScolaire.objects.all()
    eleves=Eleve.objects.all()
    context={
                "eleves":eleves,
                "niveaus":niveaus,
                "groupes":groupes,
                "annes":annes,
        }
    return render(request,'eleve/eleve.html',context)



def formeleve(request):
    niveaus=Niveau.objects.all()
    groupes=GroupeClasse.objects.all()
    annes=AnneeScolaire.objects.all()
    eleves=Eleve.objects.all()
    context={
                "eleves":eleves,
                "niveaus":niveaus,
                "groupes":groupes,
                "annes":annes,
        }

    return render(request,'eleve/ajout_eleve.html',context)


def forme_modifie(request):
    niveaus=Niveau.objects.all()
    groupes=GroupeClasse.objects.all()
    annes=AnneeScolaire.objects.all()
    eleves=Eleve.objects.all()
    context={
                "eleves":eleves,
                "niveaus":niveaus,
                "groupes":groupes,
                "annes":annes,
        }

    return render(request,'eleve/ajout_modifier.html',context)




def ajout(request):
    if request.method == 'POST':
        niveau = request.POST.get('nive')
        groupe = request.POST.get('group')
        annee = request.POST.get('anne')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        genre = request.POST.get('sexe')
        contact = request.POST.get('contact')
        photo = request.FILES.get('photo')
        naissance = request.POST.get('date')
        lieu = request.POST.get('lieu')
        pere = request.POST.get('pere')
        fonction_pere = request.POST.get('fp')
        contact_pere = request.POST.get('cp')
        mere = request.POST.get('mere')
        fonction_mere = request.POST.get('fm')
        cm = request.POST.get('cm')

        # Vérification si l'élève existe déjà
        if Eleve.objects.filter(telephone=contact).exists():
            messages.error(request, "Un élève avec ce numéro de téléphone existe déjà.")
            return render(request, 'eleve/ajout.html')

        # Création de l'élève
        eleve = Eleve.objects.create(
            groupe_classe=get_object_or_404(GroupeClasse, id=groupe),
            annee_scolaire=get_object_or_404(AnneeScolaire, id=annee),
            niveau=get_object_or_404(Niveau, id=niveau),
            nom=nom,
            prenom=prenom,
            date_naissance=naissance,
            genre=genre,
            telephone=contact,
            lieu_naissance=lieu,
            photo=photo,
            contact_mere=cm,
            mere=mere,
            profession_mere=fonction_mere,
            profession_pere=fonction_pere,
            pere=pere,
            contact_parent=contact_pere
        )

        # Récupération des frais de scolarité
        niveau_obj = get_object_or_404(Niveau, id=niveau)
        montant_total = niveau_obj.montant_frais
        tranche1 = montant_total / 2
        tranche2 = montant_total / 2

        # Création des frais de scolarité
        frais_scolarite = FraisScolarite.objects.create(
            eleve=eleve,
            annee_scolaire=eleve.annee_scolaire.nom,
            tranche1=tranche1,
            tranche2=tranche2,
            montant_total=montant_total,
            solde=tranche2  # Le solde est la deuxième tranche
        )

        # Création du reçu pour la première tranche
        recu = Recu.objects.create(
            frais_scolarite=frais_scolarite,
            montant=tranche1,
            details=f"Premier paiement des frais de scolarité pour l'année scolaire {eleve.annee_scolaire.nom}"
        )

        # Message de succès
        messages.success(request, f"L'élève {prenom} {nom} a été ajouté avec succès et le premier paiement a été effectué.")

        # Redirection vers une page d'affichage du reçu
        return redirect('afficher_recu', recu_id=recu.id)
    else:
        return render(request, 'eleve/ajout.html')
    
#AFFICHARGE DES RECUS 
def afficher_recu(request, recu_id):
        recu = get_object_or_404(Recu, id=recu_id)
        return render(request, 'eleve/afficher.html', {'recu': recu})

#FONCTION DE MODIFICATION
def modifier(request):

    if request.method=='POST':
        niveau=request.POST.get('nive')
        groups=request.POST.get('group')
        annee=request.POST.get('anne')
        nom=request.POST.get('nom')
        prenom=request.POST.get('prenom')
        genre=request.POST.get('sexe')
        contact=request.POST.get('contact')
        photo=request.POST.get('photo')
        naissance=request.POST.get('date')
        lieu=request.POST.get('lieu')
        pere=request.POST.get('pere')
        fonction_pere=request.POST.get('fp')
        contact_pere=request.POST.get('cp')
        mere=request.POST.get('mere')
        fonction_mere=request.POST.get('fm')
        cm=request.POST.get('cm')
    
       
        pk=request.POST.get('id')
        eleve=get_object_or_404(Eleve,id=pk)
        
        eleve.niveau=get_object_or_404(Niveau,id=niveau)
        eleve.groupe_classe=get_object_or_404(GroupeClasse,id=groups)
        eleve.annee_scolaire=get_object_or_404(AnneeScolaire,id=annee)
        eleve.nom=nom
        eleve.prenom=prenom
        eleve.date_naissance=naissance
        eleve.genre=genre
        eleve.telephone=contact
        eleve.lieu_naissance=lieu
        eleve.photo=photo
        eleve.Contact_mere=cm
        eleve.mere=mere
        eleve.profession_mere=fonction_mere
        eleve.profession_pere=fonction_pere
        eleve.pere=pere
        eleve.Contact_parent=contact_pere


        eleve.save()

        return redirect('eleve')
    else:
            return redirect('eleve')
    
    #FONCTION DE SUPPRESSION DES INFORMATIONS




     #FONCTION DE SUPPRESSION DES INFORMATIONS

def  supprimer(request,pk):
    eleve=get_object_or_404(Eleve,id=pk)
    eleve.delete()

    return redirect('eleve')


#FONCTION DE PAIEMENT ET RECU DE PAIEMENT DES FRAIS SCOLARITES

from django.shortcuts import render, redirect
from eleve.models import FraisScolarite,Recu

from django.contrib import messages


#SELECTIONNER L'ELEVE ANVANT D'EFFETUER SON PAIEMENT
def eleve_selection(request):
    """Vue pour afficher les filtres et la liste des élèves selon les critères."""
    niveaux = Niveau.objects.all()
    annees_scolaires = AnneeScolaire.objects.all()
    groupeclasses = GroupeClasse.objects.all()
    eleves = None

    if request.method == "POST":
        annee_scolaire_nom = request.POST.get("annee_scolaire")
        niveau_nom = request.POST.get("niveau")
        groupeclasse_nom = request.POST.get("groupeclasse")

        if annee_scolaire_nom and niveau_nom and groupeclasse_nom:
            eleves = Eleve.objects.filter(
                annee_scolaire__nom=annee_scolaire_nom,
                niveau__nom=niveau_nom,
                groupe_classe__nom=groupeclasse_nom
            )

    return render(
        request,
        'eleve/configuration_niveaux.html',
        {
            'niveaux': niveaux,
            'annees_scolaires': annees_scolaires,
            'groupeclasses': groupeclasses,
            'eleves': eleves,
        }
    )

from django.shortcuts import redirect

def payer_tranche2(request, eleve_id):
    """Vue pour effectuer le paiement de la deuxième tranche et afficher le reçu."""
    eleve = get_object_or_404(Eleve, id=eleve_id)
    frais = FraisScolarite.objects.filter(eleve=eleve, annee_scolaire=eleve.annee_scolaire.nom).first()

    if not frais:
        return render(request, 'eleve/recu_paiement.html', {'message': "Aucun frais trouvé pour cet élève."})

    if frais.solde > 0 and not frais.est_paye_tranche2:
        montant_a_payer = frais.tranche2 if frais.solde >= frais.tranche2 else frais.solde
        frais.total_paye += montant_a_payer
        frais.solde -= montant_a_payer
        frais.est_paye_tranche2 = frais.solde == 0
        frais.save()

        recu = Recu.objects.create(
            frais_scolarite=frais,
            montant=montant_a_payer,
            details=f"Deuxième paiement pour {eleve.nom} {eleve.prenom}."
        )

        return render(request, 'eleve/recu_paiement.html', {'recu': recu})

    return render(request, 'eleve/recu_paiement.html', {'message': "Le paiement de la deuxième tranche a déjà été effectué."})

#AFFICHER LES ELEVES QUI ON PAYER LA TOTALITE DES FRAIS DE SCOLARITE

from django.shortcuts import render
from .models import Eleve, FraisScolarite, Niveau, GroupeClasse, AnneeScolaire

def liste_eleves(request):
    # Récupérer tous les niveaux, groupes et années scolaires pour les filtres
    niveaux = Niveau.objects.all()
    groupes = GroupeClasse.objects.all()
    annees_scolaires = AnneeScolaire.objects.all()

    # Récupérer les paramètres de filtrage depuis la requête GET
    niveau_id = request.GET.get('niveau')
    groupe_id = request.GET.get('groupe_classe')
    annee_id = request.GET.get('annee_scolaire')

    # Filtrer les élèves selon les paramètres de filtrage
    eleves = Eleve.objects.all()

    if niveau_id:
        eleves = eleves.filter(niveau__id=niveau_id)  # Utiliser l'ID du niveau
    if groupe_id:
        eleves = eleves.filter(groupe_classe__id=groupe_id)  # Utiliser l'ID du groupe
    if annee_id:
        eleves = eleves.filter(annee_scolaire__id=annee_id)  # Utiliser l'ID de l'année scolaire

    # Récupérer les informations des frais pour chaque élève
    eleves_info = []
    for eleve in eleves:
        frais_scolarite = FraisScolarite.objects.filter(eleve=eleve).first()

        if frais_scolarite:
            if frais_scolarite.solde == 0:
                statut_paiement = 'Paiement complet'
            elif frais_scolarite.est_paye_tranche2:
                statut_paiement = 'Paiement partiel'
            else:
                statut_paiement = 'En attente de paiement'
        else:
            statut_paiement = 'Aucune donnée de paiement'

        eleves_info.append({
            'eleve': eleve,
            'statut_paiement': statut_paiement,
        })

    return render(request, 'eleve/liste_eleves.html', {
        'eleves_info': eleves_info,
        'niveaux': niveaux,
        'groupes': groupes,
        'annees_scolaires': annees_scolaires,
        'request': request
    })

