
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
    path('configuration/',views.eleve_selection,name='configuration'),
    path('recu/<int:recu_id>/', views.afficher_recu, name='afficher_recu'),
    path('payer_tranche2/<int:eleve_id>/', views.payer_tranche2, name='payer_tranche2'),
    # path('recu2/<int:recu_id>/', views.afficher_recu, name='afficher_recu'),
    path('liste-eleves/', views.liste_eleves, name='liste_eleves'),


]
