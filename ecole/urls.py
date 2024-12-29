
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
    path('ajout/',include('enseignant.urls')), # Ajout des informations
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

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

