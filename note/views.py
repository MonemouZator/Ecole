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
