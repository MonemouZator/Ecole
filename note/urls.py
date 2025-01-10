

from django.urls import path
from . import views

urlpatterns = [

    # autres modèles d'URL
    path('note', views.note, name='note'),  # Assurez-vous que le nom correspond
    path('ajout-note/',views.ajout_note,name='ajout-note'),# Chemin d'ajout  des informations
    path('modifie-note/',views.modifier,name='modifi-note'),# Chemin de modification  des informations
    path('supprime/<pk>/',views.supprimer,name='supprimer-note'),
   






]
