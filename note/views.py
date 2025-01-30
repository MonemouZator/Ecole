from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from matiere.models import Matiere
from eleve.models import Eleve
from annee_scolaire.models import AnneeScolaire
from note.models import Note
from groupe_classe.models import GroupeClasse
# Create your views here.

def note(request):
    matires=Matiere.objects.all()
    notes=Note.objects.all()
    annes=AnneeScolaire.objects.all()
    eleves=Eleve.objects.all()

    context={
                    "matires":matires,
                    "notes":notes,
                    "annes":annes,
                    "eleves":eleves
                }

    return render(request,'note/note.html',context)

# FONCTION D'ENREGISTREMENT DES ENSEIGNANTS

def ajout_note(request):

    if request.method=='POST':
        eleve=request.POST.get('eleve')
        matiere=request.POST.get('mat')
        anne=request.POST.get('anne')
        notecours=request.POST.get('nc')
        notecompo=request.POST.get('nco')
        trimestre=request.POST.get('trimestre')
        note=Note.objects.create(

            eleve=get_object_or_404(Eleve,id=eleve),
            matiere=get_object_or_404(Matiere,id=matiere),
            annee_scolaire=get_object_or_404(AnneeScolaire,id=anne),
            note_cours=notecours,
            note_comp=notecompo,
            trimestre=trimestre,
           
          
        )
        note.save()

        return redirect('note')
    else:
        return redirect('note')
    
    
def modifier(request):

    if request.method=='POST':
            eleve=request.POST.get('eleve')
            matiere=request.POST.get('mat')
            anne=request.POST.get('anne')
            notecours=request.POST.get('nc')
            notecompo=request.POST.get('nco')
            trimestre=request.POST.get('trimestre')
            pk=request.POST.get('id')
            note=get_object_or_404(Note,id=pk)
           
          
            note.eleve=get_object_or_404(Eleve,id=eleve)
            note.matiere=get_object_or_404(Matiere,id=matiere)
            note.annee_scolaire=get_object_or_404(AnneeScolaire,id=anne)
            note.note_cours=notecours
            note.note_comp=notecompo
            note.trimestre=trimestre
    
            note.save()

            return redirect('note')
    else:
            return redirect('note')
    
    #FONCTION DE SUPPRESSION DES INFORMATIONS




     #FONCTION DE SUPPRESSION DES INFORMATIONS

def  supprimer(request,pk):
    note=get_object_or_404(Note,id=pk)
    note.delete()

    return redirect('note')


###############################################################khjkihkjhj
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Eleve, Note
from niveau.models import Niveau
from groupe_classe.models import GroupeClasse
from annee_scolaire.models import AnneeScolaire
from matiere.models import Matiere

def attribuer_notes(request):
    # Récupérer les données nécessaires pour le formulaire de filtrage
    niveaux = Niveau.objects.all()
    groupes = GroupeClasse.objects.all()
    annees_scolaires = AnneeScolaire.objects.all()
    matieres = Matiere.objects.all()
    
    # Filtrer les élèves en fonction des critères sélectionnés
    eleves = Eleve.objects.all()
    if request.GET.get('niveau'):
        eleves = eleves.filter(niveau_id=request.GET['niveau'])
    if request.GET.get('groupe_classe'):
        eleves = eleves.filter(groupe_classe_id=request.GET['groupe_classe'])
    if request.GET.get('annee_scolaire'):
        eleves = eleves.filter(annee_scolaire_id=request.GET['annee_scolaire'])
    
    # Gérer l'ajout ou la mise à jour des notes
    if request.method == "POST":
        eleve_id = request.POST.get('eleve')
        annee_id = request.POST.get('anne')
        matiere_id = request.POST.get('mat')
        trimestre = request.POST.get('trimestre')
        note_cours = request.POST.get('nc')
        note_compo = request.POST.get('nco')
        
        if eleve_id and annee_id and matiere_id:
            eleve = get_object_or_404(Eleve, id=eleve_id)
            annee = get_object_or_404(AnneeScolaire, id=annee_id)
            matiere = get_object_or_404(Matiere, id=matiere_id)
            
            # Créer ou mettre à jour la note
            note, created = Note.objects.update_or_create(
                eleve=eleve,
                annee_scolaire=annee,
                matiere=matiere,
                trimestre=trimestre,
                defaults={
                    'note_cours': note_cours,
                    'note_comp': note_compo,
                },
            )
            if created:
                messages.success(request, "Note ajoutée avec succès.")
            else:
                messages.success(request, "Note mise à jour avec succès.")
        else:
            messages.error(request, "Veuillez remplir tous les champs du formulaire.")
        
        return redirect('attribuer-notes')

    # Rendre le template avec le contexte
    context = {
        'niveaux': niveaux,
        'groupes': groupes,
        'annees_scolaires': annees_scolaires,
        'eleves': eleves,
        'matieres': matieres,
    }
    return render(request, 'note/rechercher_eleve.html', context)
