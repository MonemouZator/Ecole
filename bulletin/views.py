from django.shortcuts import render
from .models import BulletinTrimestriel,BulletinAnnuel
from annee_scolaire.models import AnneeScolaire
from niveau.models import Niveau
from groupe_classe.models import GroupeClasse
from django.db.models import Avg,F
from eleve.models import Eleve
from note.models import Note

def bulletin_trimestriel(request):
    # Récupérer les niveaux et années scolaires
    niveaux = Niveau.objects.all()
    annees_scolaires = AnneeScolaire.objects.all()

    # Récupérer les paramètres de filtrage
    niveau_id = request.GET.get('niveau')
    annee_scolaire_id = request.GET.get('annee_scolaire')
    trimestre = request.GET.get('trimestre')

    # Filtrer les notes en fonction des critères sélectionnés
    notes = Note.objects.all()

    if niveau_id:
        notes = notes.filter(eleve__groupe_classe__id=niveau_id)
    if annee_scolaire_id:
        notes = notes.filter(annee_scolaire_id=annee_scolaire_id)
    if trimestre:
        notes = notes.filter(trimestre=trimestre)

    # Grouper les données par élève et calculer les moyennes
    bulletins_trimestriels = {}
    for note in notes:
        eleve = note.eleve
        if eleve.id not in bulletins_trimestriels:
            bulletins_trimestriels[eleve.id] = {
                'eleve': eleve,
                'notes_par_matiere': [],
                'moyenne_totale': 0,
            }
        bulletins_trimestriels[eleve.id]['notes_par_matiere'].append({
            'matiere__nom': note.matiere.nom,
            'moyenne_matiere': note.moyenne,
        })
        bulletins_trimestriels[eleve.id]['moyenne_totale'] += note.moyenne

    # Calculer la moyenne trimestrielle pour chaque élève
    for bulletin in bulletins_trimestriels.values():
        total_notes = len(bulletin['notes_par_matiere'])
        if total_notes > 0:
            bulletin['moyenne_totale'] = round(bulletin['moyenne_totale'] / total_notes, 2)

    # Classement des bulletins par moyenne trimestrielle
    bulletins_trimestriels_avec_moyenne = sorted(
        bulletins_trimestriels.values(), key=lambda b: b.get('moyenne_totale', 0), reverse=True
    )

    # Calcul du rang et de l'observation
    for idx, bulletin in enumerate(bulletins_trimestriels_avec_moyenne):
        bulletin['rang'] = idx + 1
        if bulletin['moyenne_totale'] >= 16:
            bulletin['observation'] = "Très Bien"
        elif bulletin['moyenne_totale'] >= 12:
            bulletin['observation'] = "Bien"
        elif bulletin['moyenne_totale'] >= 10:
            bulletin['observation'] = "Passable"
        else:
            bulletin['observation'] = "Insuffisant"

    context = {
        'bulletins_trimestriels': bulletins_trimestriels_avec_moyenne,
        'niveaux': niveaux,
        'annees_scolaires': annees_scolaires,
        'niveau_id': niveau_id,
        'annee_scolaire_id': annee_scolaire_id,
        'trimestre': trimestre,
    }

    return render(request, 'bulletins/bulletins_trimestriels.html', context)


   
  

def bulletin_annuel(request):
    niveaux = Niveau.objects.all()
    annees_scolaires = AnneeScolaire.objects.all()
    
    niveau_id = request.GET.get('niveau')
    annee_scolaire_id = request.GET.get('annee_scolaire')

    bulletins_annuels = BulletinAnnuel.objects.all()

    if niveau_id:
        bulletins_annuels = bulletins_annuels.filter(eleve__niveau__id=niveau_id)
    
    if annee_scolaire_id:
        bulletins_annuels = bulletins_annuels.filter(annee_scolaire__id=annee_scolaire_id)

    return render(request, 'bulletins/bulletins_annuels.html', {
        'bulletins_annuels': bulletins_annuels,
        'niveaux': niveaux,
        'annees_scolaires': annees_scolaires,
        'niveau_id': niveau_id,
        'annee_scolaire_id': annee_scolaire_id,
    })



# LES BULLETINS PAR GROUPE OU OPTION
def bulletins_trimestriels_groupes(request):
    annee_scolaire_id = request.GET.get("annee_scolaire")
    groupe_classe_id = request.GET.get("groupe_classe")
    trimestre = request.GET.get("trimestre")

    # Filtrer les notes en fonction des paramètres sélectionnés
    notes = Note.objects.filter(
        eleve__groupe_classe_id=groupe_classe_id,
        annee_scolaire_id=annee_scolaire_id,
        trimestre=trimestre,
    ).select_related("matiere", "eleve", "annee_scolaire")

    # Grouper les données par élève
    bulletins = {}
    for note in notes:
        eleve = note.eleve
        if eleve.id not in bulletins:
            bulletins[eleve.id] = {
                "eleve": eleve,
                "notes_par_matiere": [],
                "moyenne_totale": 0,
            }
        bulletins[eleve.id]["notes_par_matiere"].append({
            "matiere__nom": note.matiere.nom,
            "moyenne_matiere": note.moyenne,
        })
        bulletins[eleve.id]["moyenne_totale"] += note.moyenne

    # Calculer la moyenne totale pour chaque élève
    for bulletin in bulletins.values():
        total_notes = len(bulletin["notes_par_matiere"])
        if total_notes > 0:
            bulletin["moyenne_totale"] = round(bulletin["moyenne_totale"] / total_notes, 2)

    context = {
        "bulletins_trimestriels": bulletins.values(),
        "annees_scolaires": AnneeScolaire.objects.all(),
        "groupes_classes": GroupeClasse.objects.all(),  # Remplacer niveaux par groupes_classes
    }
    return render(request, "bulletins/bulletins_option.html", context)


#Bulletin Annuel PAR GROUPE DE CLASSE ET ANNEE SCOLAIRE
from matiere.models import Matiere

from django.db.models import Avg,F

from .models import BulletinTrimestriel, BulletinAnnuel, Eleve, AnneeScolaire

def bulletins_groupe(request):
    groupeclasses = GroupeClasse.objects.all()
    annees_scolaires = AnneeScolaire.objects.all()

    groupe_classe_id = request.GET.get('groupeclasse')
    annee_scolaire_id = request.GET.get('annee_scolaire')

    if groupe_classe_id and annee_scolaire_id:
        bulletins_trimestriels = BulletinTrimestriel.objects.filter(
            eleve__groupe_classe__id=groupe_classe_id,
            annee_scolaire_id=annee_scolaire_id
        )
        bulletins_annuels = BulletinAnnuel.objects.filter(
            eleve__groupe_classe__id=groupe_classe_id,
            annee_scolaire_id=annee_scolaire_id
        )
        eleves = Eleve.objects.filter(groupe_classe__id=groupe_classe_id)
    else:
        bulletins_trimestriels = BulletinTrimestriel.objects.all()
        bulletins_annuels = BulletinAnnuel.objects.all()
        eleves = Eleve.objects.all()

    # Remplir l'observation correctement
    for bulletin_annuel in bulletins_annuels:
        if bulletin_annuel.moyenne_totale_annuelle >= 16:
            bulletin_annuel.observation = "Très bien"
        elif bulletin_annuel.moyenne_totale_annuelle >= 14:
            bulletin_annuel.observation = "Bien"
        elif bulletin_annuel.moyenne_totale_annuelle >= 12:
            bulletin_annuel.observation = "Assez bien"
        elif bulletin_annuel.moyenne_totale_annuelle >= 10:
            bulletin_annuel.observation = "Passable"
        else:
            bulletin_annuel.observation = "Médiocre"

        # Enregistrer l'observation si nécessaire
        bulletin_annuel.save()

    context = {
        'groupeclasses': groupeclasses,
        'annees_scolaires': annees_scolaires,
        'bulletins_trimestriels': bulletins_trimestriels,
        'bulletins_annuels': bulletins_annuels,
        'eleves': eleves,
    }

    return render(request, 'bulletins/bulletins_groupe_annuel.html', context)

 

#  RESUTALTS DES BULLETINS
def resultat_groupe(request):
    groupe_classe_id = request.GET.get('groupe_classe')
    annee_scolaire_id = request.GET.get('annee_scolaire')
    trimestre = request.GET.get('trimestre')

    # Récupération des données pour les champs de sélection
    groupes_classes = GroupeClasse.objects.all()
    annees_scolaires = AnneeScolaire.objects.all()

    # Validation des paramètres requis
    if not groupe_classe_id or not annee_scolaire_id or not trimestre:
        return render(request, 'bulletins/resultat_annuel_classe.html', {
            'error_message': 'Veuillez sélectionner tous les filtres nécessaires.',
            'groupes_classes': groupes_classes,
            'annees_scolaires': annees_scolaires,
        })

    # Récupération des bulletins du groupe classe, année scolaire et trimestre sélectionnés
    bulletins = BulletinTrimestriel.objects.filter(
        eleve__groupe_classe_id=groupe_classe_id,
        annee_scolaire_id=annee_scolaire_id,
        trimestre=trimestre
    )

    # Ajout des moyennes et observations
    bulletins_with_data = []
    for bulletin in bulletins:
        moyenne = bulletin.moyenne_totale or 0
        if moyenne >= 19:
            observation = "Excellent"
        elif moyenne >= 17:
            observation = "Très bien"
        elif moyenne >= 14:
            observation = "Bien"
        elif moyenne >= 12:
            observation = "Assez Bien"

        elif moyenne >= 10:
            observation = "passable"
        else:
            observation = "Mediocre"

        bulletins_with_data.append({
            'bulletin': bulletin,
            'moyenne': moyenne,
            'observation': observation,
        })

    sorted_bulletins = sorted(
        bulletins_with_data,
        key=lambda b: b['moyenne'],
        reverse=True
    )

    # Calcul des rangs
    for index, data in enumerate(sorted_bulletins):
        data['rang'] = index + 1

    return render(request, 'bulletins/resultat_annuel_classe.html', {
        'groupes_classes': groupes_classes,
        'annees_scolaires': annees_scolaires,
        'sorted_bulletins': sorted_bulletins,
    })

 
# RESULTAT ANNUEL PAR GROUPE DE CLASSE OU OPTION EN FONCTION DE L'ANNEE SCOLAIRE

def resultat_annuel(request):
    groupe_classe_id = request.GET.get('groupe_classe')
    annee_scolaire_id = request.GET.get('annee_scolaire')

    # Récupération des groupes de classes et des années scolaires pour le formulaire
    groupes_classes = GroupeClasse.objects.all()
    annees_scolaires = AnneeScolaire.objects.all()

    # Debug : Imprimer les valeurs des paramètres
    print(f"groupe_classe_id: {groupe_classe_id}, annee_scolaire_id: {annee_scolaire_id}")

    # Validation des paramètres requis
    if not groupe_classe_id or not annee_scolaire_id:
        return render(request, 'bulletins/resultat_annuel.html', {
            'error_message': 'Veuillez sélectionner tous les filtres nécessaires.',
            'groupes_classes': groupes_classes,
            'annees_scolaires': annees_scolaires,
        })

    # Récupération des bulletins annuels pour le groupe de classe et l'année scolaire sélectionnés
    bulletins_annuels = BulletinAnnuel.objects.filter(
        eleve__groupe_classe_id=groupe_classe_id,
        annee_scolaire_id=annee_scolaire_id
    )

    # Debug : Vérifier si des bulletins sont récupérés
    print(f"Bulletins récupérés: {bulletins_annuels.count()}")

    # Si aucun bulletin n'est trouvé
    if bulletins_annuels.count() == 0:
        return render(request, 'bulletins/resultat_annuel.html', {
            'error_message': 'Aucun bulletin trouvé pour les critères sélectionnés.',
            'groupes_classes': groupes_classes,
            'annees_scolaires': annees_scolaires,
        })

    # Ajout des moyennes annuelles et observations
    bulletins_with_data = []
    for bulletin in bulletins_annuels:
        # Utilisation des propriétés pour récupérer les moyennes par trimestre et la moyenne annuelle
        moyennes = bulletin.moyenne_totale_par_trimestre
        moyenne_annuelle = bulletin.moyenne_totale_annuelle

        # Définition de l'observation en fonction de la moyenne annuelle
        if moyenne_annuelle >= 19:
            observation = "Excellent"
        elif moyenne_annuelle >= 17:
            observation = "Très bien"
        elif moyenne_annuelle >= 14:
            observation = "Bien"
        elif moyenne_annuelle >= 12:
            observation = "Assez Bien"
        elif moyenne_annuelle >= 10:
            observation = "Passable"
        else:
            observation = "Médiocre"

        bulletins_with_data.append({
            'bulletin': bulletin,
            'moyenne_t1': moyennes['moyenne_t1'],
            'moyenne_t2': moyennes['moyenne_t2'],
            'moyenne_annuelle': moyenne_annuelle,
            'observation': observation,
        })

    # Tri des bulletins par moyenne annuelle (par ordre décroissant)
    sorted_bulletins = sorted(bulletins_with_data, key=lambda b: b['moyenne_annuelle'], reverse=True)

    # Calcul des rangs
    for index, data in enumerate(sorted_bulletins):
        data['rang'] = index + 1

    return render(request, 'bulletins/resultat_annuel.html', {
        'groupes_classes': groupes_classes,
        'annees_scolaires': annees_scolaires,
        'sorted_bulletins': sorted_bulletins,
    })

#VALIDATION DES BULLETINS TRIMESTRIELL ET ANNUELS


#CREATION DES BULLETINS

from django.shortcuts import render, redirect
from django.contrib import messages
from eleve.models import Eleve
from annee_scolaire.models import AnneeScolaire
from groupe_classe.models import GroupeClasse
from .models import BulletinTrimestriel

def valider_bulletin_trimestre(request):
    if request.method == 'POST':
        annee_scolaire_id = request.POST.get('annee_scolaire')
        groupe_classe_id = request.POST.get('groupe_classe')
        trimestre = request.POST.get('trimestre', 1)  # Par défaut, trimestre 1 si non spécifié

        # Vérifiez que les champs sont remplis
        if not annee_scolaire_id or not groupe_classe_id:
            messages.error(request, "Veuillez sélectionner une année scolaire et un groupe de classe.")
            return redirect('valider-bulletin-trimestre')  # Remplacez par le nom de votre URL

        # Récupérer les données sélectionnées
        try:
            annee_scolaire = AnneeScolaire.objects.get(id=annee_scolaire_id)
            groupe_classe = GroupeClasse.objects.get(id=groupe_classe_id)
        except (AnneeScolaire.DoesNotExist, GroupeClasse.DoesNotExist):
            messages.error(request, "Les données sélectionnées sont invalides.")
            return redirect('trimestre')

        # Récupérer les élèves du groupe de classe
        eleves = Eleve.objects.filter(groupe_classe=groupe_classe, annee_scolaire=annee_scolaire)

        if not eleves.exists():
            messages.warning(request, "Aucun élève trouvé pour ce groupe de classe et cette année scolaire.")
            return redirect('trimestre')

        # Créer les bulletins trimestriels pour chaque élève
        for eleve in eleves:
            # Vérifier si le bulletin existe déjà
            bulletin_existe = BulletinTrimestriel.objects.filter(
                eleve=eleve,
                trimestre=trimestre,
                annee_scolaire=annee_scolaire
            ).exists()

            if not bulletin_existe:
                BulletinTrimestriel.objects.create(
                    eleve=eleve,
                    trimestre=trimestre,
                    annee_scolaire=annee_scolaire
                )

        messages.success(request, "Les bulletins ont été validés avec succès.")
        return redirect('trimestre')  # Redirigez vers la page pour afficher le succès

    # Charger les données pour le formulaire
    annees_scolaires = AnneeScolaire.objects.all()
    groupes_classes = GroupeClasse.objects.all()

    return render(request, 'bulletins/trimestre.html', {
        'annees_scolaires': annees_scolaires,
        'groupes_classes': groupes_classes,
    })


#VALIDATION DES BULLETINS ANNUELS
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BulletinAnnuel
from django.http import HttpResponseBadRequest


def valider_bulletin_annuel(request):
    if request.method == 'POST':
        annee_scolaire_id = request.POST.get('annee_scolaire')
        groupe_classe_id = request.POST.get('groupe_classe')

        # Vérifiez que les champs sont remplis
        if not annee_scolaire_id or not groupe_classe_id:
            messages.error(request, "Veuillez sélectionner une année scolaire et un groupe de classe.")
            return redirect('valider_bulletin')  # Remplacez par le nom de votre URL

        # Récupérer les données sélectionnées
        try:
            annee_scolaire = AnneeScolaire.objects.get(id=annee_scolaire_id)
            groupe_classe = GroupeClasse.objects.get(id=groupe_classe_id)
        except (AnneeScolaire.DoesNotExist, GroupeClasse.DoesNotExist):
            messages.error(request, "Les données sélectionnées sont invalides.")
            return redirect('valider_bulletin')

        # Récupérer les élèves du groupe de classe et de l'année scolaire
        eleves = Eleve.objects.filter(groupe_classe=groupe_classe, annee_scolaire=annee_scolaire)

        if not eleves.exists():
            messages.warning(request, "Aucun élève trouvé pour ce groupe de classe et cette année scolaire.")
            return redirect('valider_bulletin')

        # Créer ou valider les bulletins annuels pour chaque élève
        for eleve in eleves:
            # Vérifier si le bulletin annuel existe déjà pour l'élève et l'année scolaire
            bulletin_existe = BulletinAnnuel.objects.filter(
                eleve=eleve,
                annee_scolaire=annee_scolaire
            ).exists()

            if not bulletin_existe:
                BulletinAnnuel.objects.create(
                    eleve=eleve,
                    annee_scolaire=annee_scolaire
                )

        messages.success(request, "Les bulletins annuels ont été validés avec succès.")
        return redirect('valider_bulletin')  # Redirigez vers la page de validation

    # Charger les données pour le formulaire
    annees_scolaires = AnneeScolaire.objects.all()
    groupes_classes = GroupeClasse.objects.all()

    return render(request, 'bulletins/valider_bulletin.html', {
        'annees_scolaires': annees_scolaires,
        'groupes_classes': groupes_classes,
    })


#AFFICHER LES BULLETINS

from django.shortcuts import render,HttpResponse
from .models import Eleve, BulletinTrimestriel, BulletinAnnuel

def imprime1_view(request):
    eleves = Eleve.objects.all()  # Récupère tous les élèves
    bulletins_trimestriels = BulletinTrimestriel.objects.all()
    bulletins_annuels = BulletinAnnuel.objects.all()
    
    return render(request, 'bulletins/imprime1.html', {
        'eleves': eleves,
        'bulletins_trimestriels': bulletins_trimestriels,
        'bulletins_annuels': bulletins_annuels,
    })


 # Importer le modèle BulletinTrimestriel


def impression_bulletin(request):
    # Récupérer les paramètres de l'URL
    niveau_id = request.GET.get('niveau')
    annee_scolaire_id = request.GET.get('annee_scolaire')
    trimestre = request.GET.get('trimestre')

    # Vérifier que tous les paramètres sont bien fournis
    if not (niveau_id and annee_scolaire_id and trimestre):
        return HttpResponse("Veuillez fournir tous les paramètres nécessaires.", status=400)

    # Récupérer les bulletins filtrés
    bulletins = BulletinTrimestriel.objects.filter(
        eleve__groupe_classe__niveau_id=niveau_id,
        annee_scolaire_id=annee_scolaire_id,
        trimestre=trimestre
    ).select_related('eleve', 'annee_scolaire')

    # Vérifier s'il y a des bulletins disponibles
    if not bulletins.exists():
        return HttpResponse("Aucun bulletin trouvé pour les critères donnés.", status=404)

    # Calculer la moyenne trimestrielle pour chaque bulletin et trier après récupération
    bulletins = list(bulletins)  # Convertir en liste pour pouvoir trier après

    for bulletin in bulletins:
        # Calculer la moyenne trimestrielle (ici j'utilise la propriété moyenne_trimestrielle)
        bulletin.moyenne_trimestrielle = bulletin.moyenne_totale  # Utiliser la méthode ou la propriété pour la moyenne
        if bulletin.moyenne_trimestrielle is None:
            bulletin.moyenne_trimestrielle = 0  # Par défaut, mettre 0 si la moyenne est None

    # Trier les bulletins par moyenne_trimestrielle
    bulletins = sorted(bulletins, key=lambda b: b.moyenne_trimestrielle, reverse=True)

    # Attribuer le rang et l'observation
    for idx, bulletin in enumerate(bulletins):
        bulletin.rang = idx + 1
        if bulletin.moyenne_trimestrielle >= 16:
            bulletin.observation = "Très Bien"
        elif bulletin.moyenne_trimestrielle >= 12:
            bulletin.observation = "Bien"
        elif bulletin.moyenne_trimestrielle >= 10:
            bulletin.observation = "Passable"
        else:
            bulletin.observation = "Insuffisant"

    # Passer les bulletins au template
    context = {
        'bulletins_trimestriels': bulletins,
        'niveau_id': niveau_id,
        'annee_scolaire_id': annee_scolaire_id,
        'trimestre': trimestre,
    }

    return render(request, 'bulletins/imprime2.html', context)
