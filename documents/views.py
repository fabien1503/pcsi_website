
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateView, RedirectView, View
from django.views.generic.edit import FormView
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse, FileResponse, Http404
from django.urls import reverse

import os

from .formulaire import FormulairePosteSujet
from .models import Document, Correction
from connexion.models import Colleur





class EleveDocuments (LoginRequiredMixin, TemplateView):
	template_name="documents/documentsEleve.html"

	def get(self, request, *args, **kwargs):
		if(request.user.has_perm("documents.add_document")):
			url = reverse("profDocument")
			return HttpResponsePermanentRedirect(url)
		
		return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		#On va chercher les documents de la matière si colleur, sinon tous les documents
		try:
			matiere = self.request.user.colleur.matiere
			docs = Document.objects.filter(matiere__exact = matiere)
		except:
			docs = Document.objects.all()


		listeMatieres = []
		listeDocs = {}
		for doc in docs :
			if doc.matiere not in listeMatieres:
				listeMatieres.append(doc.matiere)
				listeDocs[doc.matiere] = {}
				for cle in Document.choixNature :
					listeDocs[doc.matiere][cle] = []

				listeDocs[doc.matiere]["matiere"] = (Colleur.choixMatiere[doc.matiere], doc.matiere)

			try :
				listeDocs[doc.matiere][doc.nature].append((doc,doc.correction))
			except:
				listeDocs[doc.matiere][doc.nature].append((doc,0))


		listeDocsByMatiere = []
		for matiere in listeMatieres:
			dic = listeDocs[matiere]
			listeDocsByMatiere.append(dic)


		context["DocByMatieres"] = listeDocsByMatiere

		return context






class ProfDocuments (PermissionRequiredMixin, FormView):
	template_name="documents/documentsProf.html"
	permission_denied_message="Vous n'avez pas les droits de profs pour accéder à cette page."
	permission_required = "documents.add_document"
	form_class = FormulairePosteSujet
	

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		#Il faut aller chercher tous les documents de la matière du professeur
		docs = Document.objects.filter(matiere__exact = self.request.user.colleur.matiere)

		listeDocs = {}
		for cle in Document.choixNature :
			listeDocs[cle] = []

		for doc in docs :
			try:
				listeDocs[doc.nature].append((doc,doc.correction))
			except:
				listeDocs[doc.nature].append((doc,0))

		listeDocs["matiere"] = [Colleur.choixMatiere[self.request.user.colleur.matiere], self.request.user.colleur.matiere]

		context["DocByMatieres"] = [listeDocs]

		return context

	
	def post(self, request, *args, **kwargs):

		form = FormulairePosteSujet(request.POST, request.FILES)
		if form.is_valid():
			if(form.cleaned_data["nature"] == "CO"):

				doc = Document.objects.get(id=request.POST["DocId"])
				corr = Correction(fichierExo=doc, titre=form.cleaned_data["titre"], fichier=form.cleaned_data["fichier"])
				corr.save()
				return HttpResponseRedirect("/documents/")

			else:
				doc = Document(titre=form.cleaned_data["titre"], nature=form.cleaned_data["nature"], matiere=request.user.colleur.matiere, fichier=form.cleaned_data["fichier"])
				doc.save()			
				return HttpResponseRedirect("/documents/")

		return self.get(request, *args, **kwargs)


	def get_default_redirect_url(self):
		return "/"



class ConsulterDoc (LoginRequiredMixin, View):

	def get(self, request, documentId, *args, **kwargs):
		doc = Document.objects.get(id=documentId)

		try:
			return FileResponse(open(doc.fichier.path, 'rb'), content_type='application/pdf')
		except FileNotFoundError:
			raise Http404()

class ConsulterCorr (LoginRequiredMixin, View):
	def get(self, request, correctionId, *args, **kwargs):
		corr = Correction.objects.get(id=correctionId)

		try:
			return FileResponse(open(corr.fichier.path, 'rb'), content_type='application/pdf')
		except FileNotFoundError:
			raise Http404()



class Supprimer (PermissionRequiredMixin, RedirectView):
	permission_denied_message="Vous n'avez pas les droits de profs pour accéder à cette page."
	permission_required = "documents.add_document"

	def get(self, request, *args, **kwargs):
		#On va cherhcher le document à supprimer
		document = Document.objects.get(id=kwargs["documentId"])
		#On supprime le fichier et éventuellement sa correction
		try:
			os.remove(document.correction.fichier.path)
		except :
			pass
		os.remove(document.fichier.path)
		#On supprime le document de la bdd
		document.delete()
		#On redirige vers la page document
		url = reverse("profDocument")
		return HttpResponseRedirect(url)