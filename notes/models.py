from django.db import models
#from django.contrib.auth.models import User
from connexion.models import Myuser, Colleur
from datetime import date



class GroupColle(models.Model):
	semestre = models.IntegerField(choices=[(1,1),(2,2)])
	numero = models.IntegerField()
	eleves = models.ManyToManyField(Myuser, limit_choices_to= models.Q(colleur=None))

	def __str__(self):
		return f'groupe {self.numero}'

	def listeEleves(self):
		liste = []
		for eleve in self.eleves.all():
			liste.append(eleve)
		return liste



class Colle(models.Model):
	colleur = models.ForeignKey(Colleur, on_delete=models.CASCADE, limit_choices_to= ~models.Q(colleur=None))
	date = models.DateField(default=date.today)
	groupColle = models.ForeignKey(GroupColle, on_delete=models.CASCADE)
	semestre = models.IntegerField(choices=[(1,1),(2,2)])
	horaire = models.TimeField(blank=True, null=True)
	salle = models.CharField(max_length=5, blank=True, default="")
	sujet = models.CharField(max_length=25, blank=True, default="")

	def eleves(self):
		return self.groupColle.listeEleves()


	def __str__(self):
		return f"colle du {self.date} avec {self.colleur.colleur}"

	class Meta:
		ordering=["date"]

class Note(models.Model):
	eleve = models.ForeignKey(Myuser, on_delete=models.CASCADE, limit_choices_to= models.Q(colleur=None))
	valeur = models.CharField(max_length=2)
	colle = models.ForeignKey(Colle, on_delete=models.CASCADE)

	class Meta:
		ordering=["colle"]


