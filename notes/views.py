
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import FormMixin
from django.views.generic.base import TemplateView, RedirectView, View
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse

from .models import Note, Colle, GroupColle
from connexion.models import Colleur
from config.semestre import get_semestre

import datetime


class EleveNotes(LoginRequiredMixin, TemplateView):
	template_name = "notes/noteEleve.html"


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		notesEleve = Note.objects.filter(eleve_id__exact=self.request.user.id).select_related("colle")

		listeMatieres = self.listeMatieres(notesEleve)

		listeRetourByMatiere = []
		
		for matiere in listeMatieres:
			notesEleveByMatiere = notesEleve.filter(colle__colleur__matiere__exact=matiere[0])
			listeSemestre = self.listeSemestre(notesEleveByMatiere)
			listeNotesBySemestre = []

			for semestre in listeSemestre:
				notes = notesEleveByMatiere.filter(colle__semestre__exact=semestre)
				listeColleur = []
				listeDate=[]
				listeValeur=[]
				for note in notes:
					listeColleur.append(note.colle.colleur)
					listeDate.append(note.colle.date)
					listeValeur.append(note.valeur)

				moyenne = round(self.calculerMoyenne(listeValeur),2)

				listeNotesBySemestre.append({"semestre": semestre, "listeColleur": listeColleur, "listeDate":listeDate, "listeValeur":listeValeur, "moyenne": moyenne})

			listeRetourByMatiere.append({"matiere": matiere, "listeNotes":listeNotesBySemestre})

		context["NotesByMatiere"] = listeRetourByMatiere

		return context


	def get(self, request, *args, **kwargs):
		if(request.user.has_perm("notes.add_colle")):
			url = reverse("colleurNotes")
			return HttpResponsePermanentRedirect(url)
		
		return super().get(request, *args, **kwargs)


	def listeMatieres(self, notesEleve):
		listeMatieres = []
		liste = []
		for note in notesEleve:
			matiere = note.colle.colleur.matiere
			semestre = note.colle.semestre
			if matiere not in liste:
				listeMatieres.append([matiere, Colleur.choixMatiere[matiere]])
				liste.append(matiere)
	
		return listeMatieres


	def listeSemestre(self, notesEleve):
		listeSemestre = []
		for note in notesEleve:
			semestre = note.colle.semestre
			if semestre not in listeSemestre:
				listeSemestre.append(semestre)

		return listeSemestre


	def calculerMoyenne(self, listeValeur):
		l = []
		for valeur in listeValeur:
			try:
				l.append(float(valeur))
			except:
				if valeur=="A":
					l.append(0)

		return sum(l)/len(l)




class ColleurNotes(PermissionRequiredMixin, TemplateView):
	template_name="notes/noteColleur.html"
	permission_denied_message="Vous n'avez pas les droits de colleurs pour accéder à cette page."
	permission_required = "notes.add_colle"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		listeColles = Colle.objects.filter(colleur_id__exact=self.request.user.colleur.id).select_related("groupColle").reverse()

		listeRetour = []
		for colle in listeColles:
			notes = colle.note_set.all()
			dicColle = {"colle":colle, "notes": notes}
			listeRetour.append(dicColle)

		context["listeColles"] = listeRetour

		listeRetour = []
		listeGroupesColle = GroupColle.objects.prefetch_related("eleves")
		for groupe in listeGroupesColle:
			eleves = groupe.eleves.all()
			dicGroupe = {"groupe":groupe, "eleves":eleves}
			listeRetour.append(dicGroupe)

		context["listeGroupesColle"] = listeRetour

		today = datetime.date.today()
		context["aujourdhui"] = today.isoformat()
		#print(today.isoformat())

		semestre = get_semestre()
		context["semestre"]=semestre

		return context



class NouvelleColle(PermissionRequiredMixin, RedirectView):
	permission_required = "notes.add_colle"
	permission_denied_message="Vous n'avez pas les droits de colleurs pour accéder à cette page."

	def post(self, request, *args, **kwargs):
		#test des valeurs donné par la méthode POST


		#On va chercher le groupe de colle et on crée la colle
		groupColleId = request.POST["groupColle"]
		groupColle = GroupColle.objects.get(pk=groupColleId)
		colleur = Colleur.objects.get(pk=request.user.colleur.id)

		colle = Colle(colleur=colleur, groupColle=groupColle)
		colle.date = request.POST["dateColle"]
		colle.semestre = request.POST["semestre"]
		if request.POST["horaire"]!="":
			colle.horaire = request.POST["horaire"]
		colle.salle = request.POST["salle"]
		colle.sujet = request.POST["sujet"]

		colle.save()

		#Pour chaque élève du groupe, on crée la note et on l'affecte à la colle
		for eleve in groupColle.listeEleves():
			try :
				noteEleve = request.POST["noteColleEleve"+str(eleve.id)]
			except :
				print("la note de l'élève n'est pas renseigné")

			colle.note_set.create(eleve=eleve, valeur=noteEleve)

		#On enregistre la colle dans la bdd
		colle.save()


		#On rediride vers la page où en rentre les notes colleurs:
		url = reverse("colleurNotes")
		return HttpResponsePermanentRedirect(url)


class ModifierColle(PermissionRequiredMixin, RedirectView):
	permission_required = "notes.change_colle"
	permission_denied_message="Vous n'avez pas les droits de colleurs pour accéder à cette page."

	def post(self, request, *args, **kwargs):
		#test des valeurs donnés par POST

		#On va chercher la colle à modifier dans la bdd
		colle = Colle.objects.get(id=kwargs["colleId"])
		#On modifie la colle
		colle.date = request.POST["dateColle"]
		if request.POST["horaire"]!="":
			colle.horaire = request.POST["horaire"]
		colle.salle = request.POST["salle"]
		colle.sujet = request.POST["sujet"]

		#On modifie les notes de chaque élève du groupe
		for note in colle.note_set.all():
			try:
				note.valeur = request.POST["noteColleEleve"+str(note.eleve.id)]
			except :
				print("Problème d'élève dans le groupe")
			note.save()
		#On enregistre
		colle.save()

		#On rediride vers la page où en rentre les notes colleurs:
		url = reverse("colleurNotes")
		return HttpResponsePermanentRedirect(url)


class SupprimerColle(PermissionRequiredMixin, RedirectView):
	permission_required = "notes.delete_colle"
	permission_denied_message="Vous n'avez pas les droits de colleurs pour accéder à cette page."

	def get(self, request, *args, **kwargs):
		#On va chercher la colle dans la bdd et on la supprime
		colle = Colle.objects.get(id=kwargs["colleId"])

		colle.delete()

		#On rediride vers la page où en rentre les notes colleurs:
		url = reverse("colleurNotes")
		return HttpResponsePermanentRedirect(url)