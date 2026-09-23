from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class FormColle(forms.Form):
	semestre = forms.ChoiceField(label="semestre", widget=forms.RadioSelect, choices=[(1,1),(2,2)])
	date = forms.CharField(label="date", widget=forms.DateInput)
	groupeColle = forms.ChoiceField(label="Groupe de Colle")


class DocAdminForm(forms.Form):
	mois = forms.IntegerField(label="choix du semestre", validators=[MinValueValidator(0), MaxValueValidator(12)])