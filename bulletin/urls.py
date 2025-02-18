from django.urls import path
from . import views

urlpatterns = [
    path('bulletins_trimestriels/', views.bulletin_trimestriel, name='bulletins_trimestriels'),  # Affiche la page des bulletins trimestriels
    path('bulletins_annuels/', views.bulletin_annuel, name='bulletins_annuels'),  # Affiche la page des bulletins annuels
    path('bulletins-option/', views.bulletins_trimestriels_groupes, name='bulletins_option'),  # Affiche l'option groupée pour les bulletins trimestriels
    path('bulletins-groupe/', views.bulletins_groupe, name='bulletins_groupe'),  # Affiche les bulletins par groupe
    path('resultat-groupe/', views.resultat_groupe, name='resultat_groupe'),  # Affiche les résultats par groupe
    path('resultat-annuel-groupe/', views.resultat_annuel, name='resultat_annuel'),  # Affiche les résultats annuels par groupe
    path('valider-bulletin-trimestre/', views.valider_bulletin_trimestre, name='trimestre'),  # Valide le bulletin trimestriel
    path('valider-bulletin-annuel/', views.valider_bulletin_annuel, name='valider_bulletin'),  # Valide le bulletin annuel
    path('imprime1/', views.imprime1_view, name='imprime1'),  # Vue pour l'impression (probablement pour imprimer les bulletins)
    path('imprimer-bulletin/', views.impression_bulletin, name='impression_bulletin'),
#    path('imprime3/', views.imprime3, name='imprime3'),
    path('resultats-trimestriels/', views.resultats_trimestriels, name='resultats_trimestriels'),
    path('resultats-annuels/', views.resultats_annuels, name='resultats_annuels'),

]
