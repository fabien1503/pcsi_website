from django.db import models
from connexion.models import Colleur


class ProgrammeColle (models.Model):

	semaine = models.PositiveIntegerField()
	programme = models.TextField()
	matiere = models.CharField(max_length=2, choices=Colleur.choixMatiere)
