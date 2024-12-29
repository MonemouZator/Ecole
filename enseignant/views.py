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