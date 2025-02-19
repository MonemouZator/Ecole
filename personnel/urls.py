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

    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    #path('fondateur-dashboard/', views.fondateur_dashboard, name='fondateur_dashboard'),
    #path('dg-dashboard/', views.dg_dashboard, name='dg_dashboard'),
    #path('censeur-dashboard/', views.censeur_dashboard, name='censeur_dashboard'),
    path('comptable-dashboard/', views.comptable_dashboard, name='comptable_dashboard'),
    path('enseignant-dashboard/', views.enseignant_dashboard, name='enseignant_dashboard'),
    # Ajoutez d'autres URL si nécessaire
]