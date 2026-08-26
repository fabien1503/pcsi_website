from django import forms
from .models import dossierUtilisateur
from .models import Document

class FormulairePosteSujet(forms.Form):

	titre = forms.CharField(label = "Titre du document", max_length=50)
	nature = forms.ChoiceField(label="Quel est le type de document ?", choices=Document.choixNature)
	fichier = forms.FileField(label = "Fichier à uploader")
	


