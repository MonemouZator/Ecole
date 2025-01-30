
from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [

    # autres modèles d'URL
    path('', views.maitre, name='enseignant'),  # Assurez-vous que le nom correspond
    path('enseinant/',views.ajout,name='ajout-enseignant'),# Chemin d'ajout  des informations
    path('enseinant-modifier/',views.modifier,name='modifi-enseignant'),# Chemin de modification  des informations
     path('supprime/<pk>/',views.supprim,name='supprimer-enseignant'),
    path('detail/',views.detail_enseignant,name='detail'),
    path('paiement/', views.paiement_salaire, name='paiement_salaire'),
    path('depense/', views.ajouter_depense, name='depense'),
    path('bilan-financier/', views.bilan_financier, name='bilan_financier'),




]
