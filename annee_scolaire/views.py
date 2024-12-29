from django.shortcuts import render,redirect,get_object_or_404
from annee_scolaire.models import AnneeScolaire

# Create your views here.

def annee_scolaire(request):
    annees=AnneeScolaire.objects.all()

    context={
                    "annees":annees
                }

    return render(request,'annee/annee.html',context)

# FONCTION D'ENREGISTREMENT DES ENSEIGNANTS

def ajout(request):
    if request.method=="POST": 
           
            nom=request.POST.get('nom')
            debut=request.POST.get('debut')
            fin=request.POST.get('fin')
           
            ensi=AnneeScolaire.objects.create(
                nom=nom,
                date_debut=debut,
                date_fin=fin
            
            )
            ensi.save()

            return redirect('an')
    else:
        return redirect('an')
    
def modifier(request):

    if request.method=='POST':
            pk=request.POST.get('id')
            ann=get_object_or_404(AnneeScolaire,id=pk)
            nom=request.POST.get('nom')
            debut=request.POST.get('debut')
            fin=request.POST.get('fin')

            ann.nom=nom
            ann.date_debut=debut
            ann.date_fin=fin
          
            ann.save()

            return redirect('an')
    else:
            return redirect('an')
    
    #FONCTION DE SUPPRESSION DES INFORMATIONS




     #FONCTION DE SUPPRESSION DES INFORMATIONS

def  supprimer(request,pk):
    annes=get_object_or_404(AnneeScolaire,id=pk)
    annes.delete()

    return redirect('an')
