
from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [

    # autres modèles d'URL


    path('', views.maitre, name='enseignant'),  # Page d'accueil pour la gestion des enseignants
    path('enseignant/', views.ajout, name='ajout-enseignant'),  # Ajouter un enseignant
    path('modifier/<int:id>/', views.modifier, name='modifier'),  # Modifier un enseignant
    path('supprime/<int:pk>/', views.supprim, name='supprimer-enseignant'),  # Supprimer un enseignant
    path('enseignant/<int:id>/', views.enseignant_detail, name='enseignant_detail'),  # Détails d'un enseignant
    path('paiement/', views.paiement_salaire, name='paiement_salaire'),  # Paiement des salaires
    path('depense/', views.ajouter_depense, name='depense'),  # Ajouter une dépense
    path('bilan-financier/', views.bilan_financier, name='bilan_financier'),  # Bilan financier
]




