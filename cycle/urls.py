
from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [

    # autres modèles d'URL
    path('', views.cycle, name='cycle'),  # Assurez-vous que le nom correspond
    path('cs/',views.ajout,name='ajout-cycle'),# Chemin d'ajout  des informations
    path('cycle/',views.modifier,name='modifi-cycle'),# Chemin de modification  des informations
    path('supprime/<pk>/',views.supprimer,name='supprimer-cycle'),
   






]
