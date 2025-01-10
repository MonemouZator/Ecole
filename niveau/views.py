from django.shortcuts import render

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from niveau.models import Niveau
from cycle.models import Cycle

# Create your views here.

def niveau(request):
    niveaus=Niveau.objects.all()
    cycles=Cycle.objects.all()
    context={
                    "niveaus":niveaus,
                    "cycles":cycles
                }

    return render(request,'niveau/niveau.html',context)

# FONCTION D'ENREGISTREMENT DES ENSEIGNANTS

def ajout(request):

    if request.method=='POST':
        cycle=request.POST.get('cy')
        nom=request.POST.get('nom')
        niveau=Niveau.objects.create(

            cycle=get_object_or_404(Cycle,id=cycle),
            nom=nom,

          
        )
        niveau.save()

        return redirect('niveau')
    else:
        return redirect('niveau')
    
    
def modifier(request):

    if request.method=='POST':
            cycle=request.POST.get('cy')
            nom=request.POST.get('nom')
            pk=request.POST.get('id')
            niveau=get_object_or_404(Niveau,id=pk)
           
            niveau.cycle=get_object_or_404(Cycle,id=cycle)
            niveau.nom=nom
    
            niveau.save()

            return redirect('niveau')
    else:
            return redirect('niveau')
    
    #FONCTION DE SUPPRESSION DES INFORMATIONS




     #FONCTION DE SUPPRESSION DES INFORMATIONS

def  supprimer(request,pk):
    cyc=get_object_or_404(Niveau,id=pk)
    cyc.delete()

    return redirect('niveau')
