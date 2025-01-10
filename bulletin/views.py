from django.shortcuts import render
from .models import BulletinTrimestriel,BulletinAnnuel
from annee_scolaire.models import AnneeScolaire
from niveau.models import Niveau
from groupe_classe.models import GroupeClasse
from django.db.models import Avg,F
from eleve.models import Eleve
from note.models import Note


def bulletins_trimestriels(request):
    # Récupérer les paramètres de la requête
    niveau_id = request.GET.get('niveau')
    annee_scolaire_id = request.GET.get('annee_scolaire')
    trimestre = request.GET.get('trimestre')

    # Filtrer les bulletins trimestriels selon les critères
    bulletins_trimestriels = BulletinTrimestriel.objects.filter(
        annee_scolaire_id=annee_scolaire_id,
        eleve__niveau_id=niveau_id,
        trimestre=trimestre
    )

    # Récupérer les niveaux et années scolaires pour le filtre
    niveaux = Niveau.objects.all()
    annees_scolaires = AnneeScolaire.objects.all()

    # Context
    context = {
        'bulletins_trimestriels': bulletins_trimestriels,
        'niveaux': niveaux,
        'annees_scolaires': annees_scolaires,
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


def bulletins_groupe(request):
    groupeclasse_id = request.GET.get('groupeclasse')
    annee_scolaire_id = request.GET.get('annee_scolaire')

    # Filtrer les élèves en fonction du groupe_classe
    if groupeclasse_id:
        eleves = Eleve.objects.filter(groupe_classe__id=groupeclasse_id)
    else:
        eleves = Eleve.objects.all()

    bulletins = BulletinAnnuel.objects.filter(eleve__in=eleves)

    if annee_scolaire_id:
        bulletins = bulletins.filter(annee_scolaire__id=annee_scolaire_id)

    # Passer les bulletins, groupeclasses et annees_scolaires à la template
    return render(request, 'bulletins/bulletins_groupe_annuel.html', {
        'bulletins_annuels': bulletins,
        'groupeclasses': GroupeClasse.objects.all(),
        'annees_scolaires': AnneeScolaire.objects.all(),
    })
 

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
