from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Myuser


class FormConnexion(forms.Form):
	login = forms.CharField(label="login", max_length=50)
	mdp = forms.CharField(label="mot de passe", widget=forms.PasswordInput)

	login.widget.attrs.update({"placeholder":"prénom.nom"})



class InscriptionForm(UserCreationForm):
    # Rendre le champ email obligatoire (par défaut dans le modèle User, il est optionnel)
    email = forms.EmailField(required=True, label="Adresse e-mail")

    class Meta(UserCreationForm.Meta):
        model = Myuser
        # On définit l'ordre d'affichage des champs dans le formulaire
        fields = ("username", "email")

    def clean_email(self):
        """Optionnel : Empêche deux utilisateurs d'avoir la même adresse e-mail"""
        email = self.cleaned_data.get('email')
        if Myuser.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse e-mail est déjà utilisée.")
        return email