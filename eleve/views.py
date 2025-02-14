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

        # Vérification des frais de scolarité pour l'élève
        frais_scolarite = FraisScolarite.objects.filter(eleve=eleve, annee_scolaire=eleve.annee_scolaire).first()

        if not frais_scolarite:
            # Calcul du montant des frais
            niveau_obj = get_object_or_404(Niveau, id=niveau)
            montant_total = niveau_obj.montant_frais
            tranche1 = montant_total / 2
            tranche2 = montant_total / 2

            # Création des frais de scolarité pour l'élève
            frais_scolarite = FraisScolarite.objects.create(
                eleve=eleve,
                annee_scolaire=eleve.annee_scolaire.nom,
                tranche1=tranche1,
                tranche2=tranche2,
                montant_total=montant_total,
                solde=tranche2,  # Le solde initial est la deuxième tranche
                paye_tranche1=True,  # Première tranche payée lors de l'enregistrement
                paye_tranche2=False  # Deuxième tranche non payée
            )

            # Création du reçu pour le premier paiement
            recu = Recu.objects.create(
                frais_scolarite=frais_scolarite,
                montant=frais_scolarite.tranche1,
                details=f"Premier paiement des frais de scolarité pour l'année scolaire {eleve.annee_scolaire.nom}"
            )

            # Message de succès
            messages.success(request, f"L'élève {prenom} {nom} a été ajouté avec succès et le premier paiement a été effectué.")

            # Redirection vers la page d'affichage du reçu
            return redirect('eleve/affiche.html', recu_id=recu.id)
        else:
            messages.error(request, "Les frais de scolarité existent déjà pour cet élève.")
            return redirect('eleve')
    else:
        return render(request, 'eleve/affiche.html')



# Ajout de la vue pour le paiement de la deuxième tranche
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Eleve, FraisScolarite, Recu

def paiement_tranche2(request, eleve_id):
    # Récupérer l'élève et ses frais scolaires pour l'année scolaire actuelle
    eleve = get_object_or_404(Eleve, id=eleve_id)
    frais_scolarite = get_object_or_404(FraisScolarite, eleve=eleve, annee_scolaire=eleve.annee_scolaire)

    # Vérifier si la deuxième tranche a déjà été payée
    if frais_scolarite.paye_tranche2:
        messages.error(request, "La deuxième tranche a déjà été payée.")
        return redirect('afficher_frais', eleve_id=eleve.id)

    # Si la deuxième tranche n'est pas encore payée, on effectue le paiement
    frais_scolarite.paye_tranche2 = True
    frais_scolarite.solde = 0  # Le solde devient 0 après le paiement de la deuxième tranche
    frais_scolarite.save()

    # Création du reçu pour le paiement de la deuxième tranche
    recu = Recu.objects.create(
        frais_scolarite=frais_scolarite,
        montant=frais_scolarite.tranche2,
        details=f"Deuxième paiement des frais de scolarité pour l'année scolaire {eleve.annee_scolaire.nom}"
    )

    # Message de succès pour informer l'utilisateur
    messages.success(request, f"La deuxième tranche a été payée pour {eleve.prenom} {eleve.nom}.")
    
    # Rediriger vers la page du reçu pour afficher les détails
    return redirect('afficher_recu', recu_id=recu.id)



    
#AFFICHARGE DES RECUS 

#RECU DE PAIEMENT DE LA DEUXIEME TRANCHE
def afficher_recu(request, recu_id):
        recu = get_object_or_404(Recu, id=recu_id)
        return render(request, 'eleve/afficher.html', {'recu': recu})



#FONCTION DE MODIFICATION
from django.shortcuts import render, get_object_or_404, redirect
from .models import Eleve, Niveau, GroupeClasse, AnneeScolaire

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Eleve, Niveau, GroupeClasse, AnneeScolaire

def modifier(request, pk):
    # Récupérer l'élève à modifier
    eleve = get_object_or_404(Eleve, pk=pk)

    if request.method == 'POST':
        # Récupérer les données du formulaire
        niveau_id = request.POST.get('niveau')
        groupe_classe_id = request.POST.get('groupe_classe')
        annee_scolaire_id = request.POST.get('annee_scolaire')

        # Validation des relations avec les modèles
        try:
            niveau = get_object_or_404(Niveau, id=int(niveau_id)) if niveau_id else None
            groupe_classe = get_object_or_404(GroupeClasse, id=int(groupe_classe_id)) if groupe_classe_id else None
            annee_scolaire = get_object_or_404(AnneeScolaire, id=int(annee_scolaire_id)) if annee_scolaire_id else None
        except ValueError:
            messages.error(request, "Les valeurs des champs sont incorrectes.")
            return redirect('modifier_eleve', pk=pk)
        except Exception as e:
            messages.error(request, f"Une erreur est survenue : {str(e)}")
            return redirect('modifier_eleve', pk=pk)

        # Mettre à jour les informations de l'élève
        eleve.niveau = niveau
        eleve.groupe_classe = groupe_classe
        eleve.annee_scolaire = annee_scolaire  # ✅ Correctement assigné

        eleve.nom = request.POST.get('nom')
        eleve.prenom = request.POST.get('prenom')
        eleve.date_naissance = request.POST.get('date_naissance')
        eleve.lieu_naissance = request.POST.get('lieu_naissance')
        eleve.genre = request.POST.get('genre')
        eleve.telephone = request.POST.get('telephone')
        eleve.pere = request.POST.get('pere')
        eleve.profession_pere = request.POST.get('profession_pere')
        eleve.contact_parent = request.POST.get('contact_parent')
        eleve.mere = request.POST.get('mere')
        eleve.profession_mere = request.POST.get('profession_mere')
        eleve.contact_mere = request.POST.get('contact_mere')

        # Si une nouvelle photo est téléchargée, l'associer à l'élève
        photo = request.FILES.get('photo')
        if photo:
            eleve.photo = photo

        # Sauvegarder les changements
        eleve.save()

        # Ajouter un message de succès
        messages.success(request, "Les informations de l'élève ont été mises à jour avec succès.")
        return redirect('eleve')  # Rediriger vers la liste des élèves
    else:
        # Si la méthode n'est pas POST, afficher le formulaire avec les données actuelles
        niveaux = Niveau.objects.all()
        groupes = GroupeClasse.objects.all()
        annees_scolaires = AnneeScolaire.objects.all()
        context = {
            'eleve': eleve,
            'niveaux': niveaux,
            'groupes': groupes,
            'annees_scolaires': annees_scolaires,
        }
        print(f"Année scolaire de l'élève: {eleve.annee_scolaire}")

        return render(request, 'eleve/modifier_eleve.html', context)


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
    
    # Accès direct à l'objet AnneeScolaire associé à l'élève
    frais = FraisScolarite.objects.filter(eleve=eleve, annee_scolaire=eleve.annee_scolaire).first()

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



#DETAILS eleve

from django.shortcuts import render, get_object_or_404
from .models import Eleve

def eleve_detail(request, pk):
    # Récupérer l'élève avec l'ID passé en paramètre
    eleve = get_object_or_404(Eleve, id=pk)
    return render(request, 'eleve/detail.html', {'eleve': eleve})
