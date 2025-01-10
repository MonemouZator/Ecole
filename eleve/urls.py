
from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [

    # autres modèles d'URL
    path('', views.eleve, name='eleve'),  # Assurez-vous que le nom correspond
    path('fome',views.formeleve,name='forme'),
    path('fome-modif',views.forme_modifie,name='modif'),
    path('ajout/',views.ajout,name='ajout-eleve'),# Chemin d'ajout  des informations
    path('modif/',views.modifier,name='modifi-eleve'),# Chemin de modification  des informations
    path('sup/<pk>/',views.supprimer,name='supprimer-eleve'),
   






]
