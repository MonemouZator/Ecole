from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from niveau.models import Niveau
from groupe_classe.models import GroupeClasse
from annee_scolaire.models import AnneeScolaire
from eleve.models import Eleve
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




# FONCTION D'ENREGISTREMENT DES ENSEIGNANTS
def ajout(request):
    if request.method == 'POST':
        niveau = request.POST.get('nive')
        groupe = request.POST.get('group')
        annee = request.POST.get('anne')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        genre = request.POST.get('sexe')
        contact = request.POST.get('contact')
        photo = request.POST.get('photo')
        naissance = request.POST.get('date')
        lieu = request.POST.get('lieu')
        pere = request.POST.get('pere')
        fonction_pere = request.POST.get('fp')
        contact_pere = request.POST.get('cp')
        mere = request.POST.get('mere')
        fonction_mere = request.POST.get('fm')
        cm = request.POST.get('cm')

        # Création de l'objet Eleve
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
            contact_mere=cm,  # Utilisation de 'contact_mere' et non 'Contact_mere'
            mere=mere,
            profession_mere=fonction_mere,
            profession_pere=fonction_pere,
            pere=pere,
            contact_parent=contact_pere  # Utilisation de 'contact_parent' et non 'Contact_parent'
        )

        # Sauvegarde de l'objet
        eleve.save()

        return redirect('eleve')
    else:
        return redirect('eleve')

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
