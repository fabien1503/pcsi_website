from pathlib import Path
from .models import Colleur
import re
import subprocess


CHEMIN_TEMPLATE = str(Path(__file__).resolve().parent)+"/latex/template.tex"
CHEMIN_LOGO = str(Path(__file__).resolve().parent)+"/latex/"
CHEMIN_FICHIER = str(Path(__file__).resolve().parent.parent)+"/fichiersTeleverse/DocAdministratif/"

class Scribe():

	def __init__(self, user, mois, listeColles, classe = "PCSI"):
		self.user = user
		self.mois = mois
		self.listeColles = listeColles
		self.classe = classe

		self.document = ""
		self.nombreEtudiants = 0

		self.chargerTemplate()


	def chargerTemplate(self, template = CHEMIN_TEMPLATE):
		with open(template, "r") as fichierTemplate:
			for line in fichierTemplate:
				self.document += line


	def compilerDocument(self):

		cheminFichier = self.remplirDocument()

		#On compile le fichier latex pour générer le PDF
		#On prépare la commande à exécuter
		commande = [
			"pdflatex", 
			"-interaction=nonstopmode", 
			f"-output-directory={CHEMIN_FICHIER}", cheminFichier]

        #On exécute la commande
		resultat = subprocess.run(commande, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


	def remplirDocument(self):
		#On écrit le chemin du logo
		self.document = re.sub("CHEMINGRAPHIQUES", "{"+CHEMIN_LOGO+"}", self.document)
		#On écrit la discipline
		self.document = re.sub("SCRIBEDISCIPLINE", Colleur.choixMatiere[self.user.colleur.matiere], self.document)
		#On écrit la classe
		self.document = re.sub("SCRIBECLASSE", self.classe, self.document)
		#On écrit le mois
		self.document = re.sub("SCRIBEMOIS", self.mois, self.document)
		#On écrit le nom
		self.document = re.sub("SCRIBE_NOM", self.user.last_name, self.document)
		#On écrit le prénom
		self.document = re.sub("SCRIBEPRENOM", self.user.first_name, self.document)
		#On écrit le tableau
		self.document = re.sub("SCRIBETABLEAU", self.makeTableau(), self.document)
		#On écrit le nombre d'heures
		self.document = re.sub("SCRIBENOMBREHEURE", str(len(self.listeColles))+" h", self.document)
		#On écrit le nombre d'élèves
		self.document = re.sub("SCRIBENOMBREETUDIANT", str(self.nombreEtudiants), self.document)

		cheminFichier = CHEMIN_FICHIER + str(self.user.id) +".tex"
		#On crée les dossier s'ils nexiste pas
		Path(cheminFichier).parent.mkdir(parents=True, exist_ok=True)
		#On écrit tout dans le fichier .tex
		with open(cheminFichier, "w") as fichier:
			fichier.write(self.document)

		return cheminFichier
		


	def makeTableau(self):
		tableau = ""
		for colle in self.listeColles:
			ligne =""
			ligne += str(colle.date.day)+"/"+str(colle.date.month)+" & "
			heure = colle.horaire.strftime("%H:%M") if colle.horaire else ""
			ligne += heure+" & "
			ligne += colle.salle+" & "
			ligne += str(colle.groupColle.numero)+" & "
			(present, absent, listeNoms) = self.compterEleves(colle)
			ligne += listeNoms + " & "
			ligne += str(present)+" & "
			ligne += str(absent)+" & "
			ligne += str(colle.sujet)+r"\\\ \\hline"+"\n"
			tableau += ligne

		return tableau

	def compterEleves(self, colle):
		present = 0
		absent = 0
		listeNoms = ""
		compteur = 0
		listeNotes = colle.note_set.all()
		for note in listeNotes:
			compteur += 1
			if note.valeur == "A":
				absent +=1
			else:
				present += 1
			if compteur != len(listeNotes):
				listeNoms += note.eleve.last_name + ", "
			else:
				listeNoms += note.eleve.last_name
		self.nombreEtudiants += absent + present
		return present, absent, listeNoms


