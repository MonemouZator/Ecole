
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    
    # LES CHEMINS POUR LA TABLE PERSONNELE

    path('admin/', admin.site.urls),
    path('',include('personnel.urls')),

    # LES CHEMINS POUR LA TABLE ENSEIGNANT
    path('enseignant/',include('enseignant.urls')), # Affichager de la page
    path('ajout-enseignant/',include('enseignant.urls')), # Ajout des informations
    path('modification/',include('enseignant.urls')), # Ajout des informations
    path('suppression/',include('enseignant.urls')), # Ajout des informations
    path('detail-enseignant/',include('enseignant.urls')),

# LES CHEMIN DE ANNEE SCOLAIRE
    path('annee-scolaire/',include('annee_scolaire.urls')),
    path('ajout-scolaire/',include('annee_scolaire.urls')),
    path('modifie-scolaire/',include('annee_scolaire.urls')),
    path('supprime-scolaire/',include('annee_scolaire.urls')),
  
# LES CHEMIN DES CYCLES
    path('cycle-scolaire/',include('cycle.urls')),
    path('ajout-cycle/',include('cycle.urls')),
    path('modifie-cycle/',include('cycle.urls')),
    path('supprime-cycle/',include('cycle.urls')),
    
# LES CHEMIN DES NIVEAUX
    path('niveau/',include('niveau.urls')),
    path('ajout-niveau/',include('niveau.urls')),
    path('modifie-niveau/',include('niveau.urls')),
    path('supprime-niveau/',include('niveau.urls')),

# LES CHEMIN DES GROUPES PEDAGOGIQUES
    path('groupe/',include('groupe_classe.urls')),
    path('ajout-groupe/',include('groupe_classe.urls')),
    path('modifie-groupe/',include('groupe_classe.urls')),
    path('supprime-groupe/',include('groupe_classe.urls')),

# LES CHEMIN DES MATIERES
    path('matiere/',include('matiere.urls')),
    path('ajout-matiere/',include('matiere.urls')),
    path('modifie-matiere/',include('matiere.urls')),
    path('supprime-matiere/',include('matiere.urls')),

    # LES CHEMIN DES MATIERES
    path('eleve/',include('eleve.urls')),
    path('affiche/',include('eleve.urls')),
    path('affiche_modif/',include('eleve.urls')),
    
    path('ajout-eleve/',include('eleve.urls')),
    path('modifie-eleve/',include('eleve.urls')),
    path('supprime-eleve/',include('eleve.urls')),

#LES CHEMIN DES MATIERES
    path('note/',include('note.urls')),
    path('ajout-note/',include('note.urls')),
    path('modifie-note/',include('note.urls')),
    path('supprime-note/',include('note.urls')),

#LES CHEMIN DES MATIERES
    path('bulletins_trimestriels/',include('bulletin.urls')),
    path('bulletins_annuels/',include('bulletin.urls')),
    path('bulletins_option/',include('bulletin.urls')),
    path('bulletins_groupe/',include('bulletin.urls')),
    path('resultat-groupe/',include('bulletin.urls')),
    path('resultat-groupe-annel/',include('bulletin.urls')),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

