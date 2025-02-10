from django.urls import path
# Importation de la fonction definie dans la Wiew
from personnel import views

urlpatterns = [

    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('administrateurs/ajouter/', views.ajout_administrateur, name='ajouter_administrateur'),  # Vue pour ajouter un administrateur
    path('liste/', views.liste_administrateurs, name='liste_administrateurs'),  # Page pour afficher la liste des administrateurs

    path('administrateur/supprimer/<int:administrateur_id>/', views.supprimer_administrateur, name='supprimer_administrateur'),
    path('bloquer/<int:utilisateur_id>/', views.bloquer_utilisateur, name='bloquer_utilisateur'),
    path('debloquer/<int:utilisateur_id>/', views.debloquer_utilisateur, name='debloquer_utilisateur'),
    path('reset/', views.password_reset_request, name='password_reset_request'),

   path('comptable/', views.comptable_dashboard, name='comptable_dashboard'),
   path('directeur/', views.directeur_dashboard, name='directeur_dashboard'),
   path('enseignant/', views.enseignant_dashboard, name='enseignant_dashboard'),

]