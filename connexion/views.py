from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.views import RedirectURLMixin
from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string


from .models import Myuser, Colleur
from notes.models import GroupColle
from config.semestre import get_semestre
from .tokens import generateur_token
from .formulaire import FormConnexion, InscriptionForm


class Index(RedirectURLMixin, FormView):
	template_name = "connexion/index.html"
	form_class = FormConnexion
	#success_url = "/"


	def form_valid(self, form):
		username = form.cleaned_data['login']
		mdp = form.cleaned_data['mdp']

		user = authenticate(self.request, username = username, password=mdp)
		if user is not None:
			login(self.request, user)
			self.success_url = self.get_success_url()
		else:
			self.extra_context = {'erreurLogin': "Erreur de login ou de mot de passe"}
			return self.form_invalid(form)

		return super().form_valid(form)

	def get_default_redirect_url(self):
		return "/"


class Inscription(CreateView):
	template_name = "connexion/inscription.html"
	form_class = InscriptionForm

	def get_success_url(self, *args, **kwargs):
		return reverse("activation_attente")

	def form_valid(self, form):
		# 1. On intercepte la création de l'utilisateur sans le sauvegarder en BDD
		user = form.save(commit=False)
		user.is_active = False # On le désactive
		#On remplie le nom et le prénom de l'utilisateur
		login = user.username
		prenom_brut, nom_brut = login.split('.')

		user.first_name = self.formater_nom(prenom_brut)
		user.last_name = self.formater_nom(nom_brut)

		user.save()

		# 2. Génération des éléments sécurisés du lien
		current_site = get_current_site(self.request)
		uid = urlsafe_base64_encode(force_bytes(user.pk))
		token = generateur_token.make_token(user)
		lien_activation = f"https://{current_site.domain}/connexion/activer/{uid}/{token}/"

		# 3. Préparation et envoi de l'e-mail HTML
		sujet = "Activez votre compte"
		message_html = render_to_string('connexion/activation_email.html', {
			'user': user,
			'lien_activation': lien_activation,
		})

		send_mail(
			subject=sujet,
			message=f"Activez votre compte ici : {lien_activation}",
			from_email=None,
			recipient_list=[user.email],
			html_message=message_html,
		)

		# 4. On appelle la méthode parente qui gère la redirection automatique vers success_url
		return super().form_valid(form)

	#fonction pour gérer la mise en forme des prénoms composés
	def formater_nom(self, texte):
		morceaux = texte.split('-')
		return "-".join(morceau.capitalize() for morceau in morceaux)


class Attente(TemplateView):
	template_name = "connexion/activation_attente.html"


def activer_compte(request, uidb64, token):
	try:
		# 1. Décoder l'ID utilisateur (uidb64) pour récupérer la clé primaire
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = Myuser.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	# 2. Vérifier si l'utilisateur existe et si le jeton de sécurité est valide
	if user is not None and generateur_token.check_token(user, token):
		user.is_active = True  # Le compte est officiellement actif
		user.save()

		# Optionnel : Connecter l'utilisateur automatiquement après activation
		login(request, user)
        
		return render(request, 'connexion/activation_reussite.html')
	else:
		# Si le lien a expiré ou s'il a déjà été utilisé
		return render(request, 'connexion/activation_echec.html')



class Deconnexion(RedirectView):
	permanent = True
	pattern_name = "index"

	def get_redirect_url(self, *args, **kwargs):
		logout(self.request)

		return super().get_redirect_url(*args, **kwargs)


class Annuaire(LoginRequiredMixin, TemplateView):
	template_name = "connexion/annuaire.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		#On récupère le semestre en cours
		semestre = get_semestre()

		#On récupère tous les groupes de colle du semestre en cours
		groupes = GroupColle.objects.filter(semestre__exact=semestre).prefetch_related("eleves")

		listeEmails =[]
		nombreEleve = 0
		for groupe in groupes :
			nombreEleve += len(groupe.listeEleves())
			for eleve in groupe.listeEleves():
				listeEmails.append(eleve.email)


		context["NbEleves"] = nombreEleve
		context["listeGroupes"] = groupes
		context["listeEmails"] = listeEmails

		#On récupère la liste des colleurs et on les classes par matières
		colleurs = Colleur.objects.all()

		listeMatiere = []
		for colleur in colleurs:
			if colleur.matiere not in listeMatiere:
				listeMatiere.append(colleur.matiere)

		listeColleursByMatiere = []
		for matiere in listeMatiere:
			liste = []
			for colleur in colleurs:
				if colleur.matiere == matiere :
					liste.append(colleur)
			listeColleursByMatiere.append((Colleur.choixMatiere[matiere], liste))

		context["listeColleur"] = listeColleursByMatiere

		return context



