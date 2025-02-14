from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#FONCTION DE LA PAGE D'ACCUEIL

@login_required
def home(request):

    services = request.session.get('services', [])
    return render(request, 'base/index.html', {'services': services})
  

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth import get_user_model

#User = get_user_model()  # Utilisation du modèle personnalisé

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Veuillez entrer votre email et mot de passe.")
            return redirect('login')

        user = authenticate(request, username=email, password=password)  # Utilisation de l'email

        if user is not None:
            login(request, user)
            messages.success(request, "Bienvenue, vous êtes connecté avec succès.")

            # Vérification du rôle de l'utilisateur et redirection appropriée
            if user.fonction == 'COMPTABLE':
                return redirect('comptable_dashboard')
            elif user.fonction == 'DG':
                return redirect('directeur_dashboard')
            elif user.fonction == 'ENSEIGNANT':
                return redirect('enseignant_dashboard')
            elif user.fonction == 'FONDATEUR':
                return redirect('home')
            else:
                # Si la fonction de l'utilisateur est invalide ou non définie
                messages.error(request, "Votre fonction est incorrecte ou manquante.")
                return redirect('login')

            return redirect('home')  # Redirection par défaut
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
            return redirect('login')

    return render(request, 'login/login.html')




@login_required
def comptable_dashboard(request):
  
    return render(request, 'login/comptable_dashboard.html')


@login_required
def directeur_dashboard(request):

    return render(request,'login/directeur_dashboard.html')

    


@login_required
def enseignant_dashboard(request):
  

     return render(request,'login/enseignant_dashboard.html')

#DECONNEXION
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige vers la page de connexion après la déconnexion

#FONCTION D'ENREGISTREMENT DES UTILISATEURS


User = get_user_model()

def ajout_administrateur(request):
    if request.method == "POST":
        print("Données reçues :", request.POST)  # Debugging
        print("Fichiers reçus :", request.FILES)

        email = request.POST.get("email")
        password = request.POST.get("password")
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        telephone = request.POST.get("telephone")
        genre = request.POST.get("genre")
        date_naissance = request.POST.get("date_naissance")
        lieu_naiss = request.POST.get("lieu_naiss")
        fonction = request.POST.get("fonction")
        photo = request.FILES.get("photo")

        if Administrateur.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect("ajouter_administrateur")

        try:
            administrateur = Administrateur.objects.create(
                username=email,
                email=email,
                nom=nom,
                prenom=prenom,
                telephone=telephone,
                genre=genre,
                date_naissance=date_naissance,
                lieu_naiss=lieu_naiss,
                fonction=fonction,
                photo=photo,
            )
            administrateur.set_password(password)
            administrateur.save()
            messages.success(request, "Administrateur ajouté avec succès !")
            return redirect("liste_administrateurs")
        except Exception as e:
            print("Erreur :", e)
            messages.error(request, f"Erreur lors de l'ajout : {e}")

    return render(request, 'login/ajouter_administrateur.html')

#LISTE DES UTILISATEURS
def liste_administrateurs(request):
    try:
        # Filtrer les administrateurs pour exclure les super utilisateurs
        administrateurs = Administrateur.objects.exclude(is_superuser=True)

        # Passer les administrateurs filtrés au template
        return render(request, 'login/liste_administrateurs.html', {'administrateurs': administrateurs})

    except Exception as e:
        # Gérer les erreurs et afficher un message si une exception se produit
        messages.error(request, f"Erreur lors du chargement des administrateurs : {e}")
        return render(request, 'login/liste_administrateurs.html', {'administrateurs': []})

#SUPPRESSION

from django.shortcuts import get_object_or_404, redirect
from .models import Administrateur

def supprimer_administrateur(request, administrateur_id):
    administrateur = get_object_or_404(Administrateur, id=administrateur_id)
    administrateur.delete()
    messages.success(request, "Administrateur supprimé avec succès.")
    return redirect('liste_administrateurs')

#FONCTION POUR BLOGUER UN UTILISATEUR
from django.contrib.auth.models import User

# Bloquer un administrateur
def bloquer_utilisateur(request, utilisateur_id):
    try:
        administrateur = Administrateur.objects.get(id=utilisateur_id)  # Assurez-vous d'utiliser Administrateur
        administrateur.is_active = False  # Bloquer l'utilisateur
        administrateur.save()

        messages.success(request, f"L'utilisateur {administrateur.username} a été bloqué avec succès.")
    except Administrateur.DoesNotExist:
        messages.error(request, "Administrateur non trouvé.")

    return redirect('liste_administrateurs')

# Débloquer un administrateur
def debloquer_utilisateur(request, utilisateur_id):
    try:
        administrateur = Administrateur.objects.get(id=utilisateur_id)  # Assurez-vous d'utiliser Administrateur
        administrateur.is_active = True  # Débloquer l'utilisateur
        administrateur.save()

        messages.success(request, f"L'utilisateur {administrateur.username} a été débloqué avec succès.")
    except Administrateur.DoesNotExist:
        messages.error(request, "Administrateur non trouvé.")

    return redirect('liste_administrateurs')


#FONCTION DE REINITIALISATION DES MOTS DE PASSE

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            try:
                # Vérifier si l'email existe dans la base de données
                user = get_user_model().objects.get(email=email)
                
                # Créer un token de réinitialisation
                token = default_token_generator.make_token(user)
                
                # Encode l'ID de l'utilisateur pour l'inclure dans l'URL
                uid = urlsafe_base64_encode(str(user.pk).encode())
                
                # Obtenir le domaine actuel pour générer l'URL complète
                domain = get_current_site(request).domain
                
                # Générer l'URL de réinitialisation
                reset_link = f'http://{domain}/reset/{uid}/{token}/'

                # Créer le message d'e-mail
                subject = 'Réinitialisation de votre mot de passe'
                message = render_to_string('login/password_reset_done.html', {
                    'reset_link': reset_link,
                    'user': user,
                })

                # Envoyer l'e-mail
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
                
                # Rediriger vers une page de confirmation
                return redirect('password_reset_done')
            except get_user_model().DoesNotExist:
                # L'utilisateur n'existe pas
                pass
    return render(request, 'login/password_reset_request.html')
