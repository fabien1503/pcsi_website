from django import forms



class FormColle(forms.Form):
	semestre = forms.ChoiceField(label="semestre", widget=forms.RadioSelect, choices=[(1,1),(2,2)])
	date = forms.CharField(label="date", widget=forms.DateInput)
	groupeColle = forms.ChoiceField(label="Groupe de Colle")
