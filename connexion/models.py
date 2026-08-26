from django.db import models
from django.contrib.auth.models import User



class Myuser(User):
	class Meta:
		proxy = True
		ordering=["last_name", "first_name"]


	def __str__(self):
		try :
			self.colleur
		except :
			return f"{self.first_name} {self.last_name}"

		return f"{Colleur.choixCivilite[self.colleur.civilite]} {self.last_name}"



class Colleur(models.Model):
	colleur = models.OneToOneField(Myuser, on_delete=models.CASCADE)

	choixCivilite = {"MR" : "Mr", "MM":"Mme"}
	civilite = models.CharField(max_length=2, choices=choixCivilite)
	choixMatiere = {"PH":"Physique","CH":"Chimie","MT":"Maths","AN":"Anglais","FR":"Français"}
	matiere = models.CharField(max_length=2, choices=choixMatiere)

	def __str__(self):
		return str(self.colleur)


