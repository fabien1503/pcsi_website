from django.db import models
from connexion.models import Colleur


def dossierUtilisateur(instance, filename):
	return "{0}/{1}".format(instance.matiere, instance.titre)

def dossierUtilisateurCorrection(instance, filename):
	return "{0}/Correction/{1}".format(instance.fichierExo.matiere, instance.titre)


class Document(models.Model):

	titre = models.CharField(max_length=50)
	matiere = models.CharField(max_length=2, choices=Colleur.choixMatiere)
	choixNature = {"TD":"TD", "DS":"DS", "CR":"Cours", "DM":"DM", "CO":"Correction"}
	nature = models.CharField(max_length=2, choices=choixNature)
	fichier = models.FileField(upload_to= dossierUtilisateur)

	class Meta:
		ordering=["titre"]

class Correction(models.Model):

	fichierExo = models.OneToOneField(Document, on_delete=models.CASCADE)
	titre = models.CharField(max_length=50)
	fichier = models.FileField(upload_to= dossierUtilisateurCorrection)
