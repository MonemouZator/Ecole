from django.urls import path
from . import views

urlpatterns = [
    path('bulletins_trimestriels/', views.bulletins_trimestriels, name='bulletins_trimestriels'),
    path('bulletins_annuels/', views.bulletin_annuel, name='bulletins_annuels'),
    path('bulletins-option/', views.bulletins_trimestriels_groupes, name='bulletins_option'),
    path('bulletins-groupe/', views.bulletins_groupe, name='bulletins_groupe'),
    path('resultat-groupe/', views.resultat_groupe, name='resultat_groupe'),
    path('resultat-annuel-groupe/', views.resultat_annuel, name='resultat_annuel'),
]

