
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, ProcessFormView, DeleteView
from django.views.generic.base import TemplateView
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse

from .models import ProgrammeColle
from connexion.models import Colleur



class Index (TemplateView):
	template_name = "progcolle/eleve.html"

	def get(self, request, *args, **kwargs):
		if(request.user.has_perm("progcolle.add_programmecolle")):
			url = reverse("progProf")
			return HttpResponsePermanentRedirect(url)
		
		return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		matieres = self.listeMatiere()

		listeProgrammes = {}
		for matiere in matieres:
			prog = ProgrammeColle.objects.filter(matiere__exact=matiere).last()
			listeProgrammes[Colleur.choixMatiere[matiere]]=prog

		context["listeProgrammes"]=listeProgrammes

		return context


	def listeMatiere(self):
		programmes = ProgrammeColle.objects.all()
		liste = []
		for prog in programmes:
			if prog.matiere not in liste:
				liste.append(prog.matiere)
		return liste



class ProgrammeContexteMixin:
    permission_denied_message = "Vous n'avez pas les droits de profs pour accéder à cette page."
    permission_required = "progcolle.add_programmecolle"
    template_name = "progcolle/index.html"

    model = ProgrammeColle
    fields = ["semaine", "programme"]

    titre_programme = ""
    titre_bouton = "Enregistrer"

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        programmes = ProgrammeColle.objects.filter(matiere__exact=self.request.user.colleur.matiere)
        context["programmes"] = programmes
        context["programme_de_la_semaine"] = programmes.last()
        context["titre_programme"]=self.titre_programme
        context["titre_bouton"]=self.titre_bouton
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse("index")



class ProgProf(ProgrammeContexteMixin, PermissionRequiredMixin, CreateView):
	titre_programme = "Nouveau programme de colle"

	def post(self, request, *args, **kwargs):

		self.object = ProgrammeColle(matiere=request.user.colleur.matiere)
		return ProcessFormView.post(self, request, *args, **kwargs)




class Modifier(ProgrammeContexteMixin, PermissionRequiredMixin, UpdateView):
	pk_url_kwarg = "programmeId"
	titre_programme = "Modifier programme de colle"
	titre_bouton = "Modifier"


class Supprimer(ProgrammeContexteMixin, PermissionRequiredMixin, DeleteView):
	titre_programme = "êtes vous sûr de vouloir supprimer ce programme de colle ?"
	titre_bouton = "Oui"
	pk_url_kwarg = "programmeId"

