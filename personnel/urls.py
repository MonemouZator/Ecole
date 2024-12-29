from django.urls import path
# Importation de la fonction definie dans la Wiew
from personnel import views

urlpatterns = [
    path('',views.home, name='home'),

]