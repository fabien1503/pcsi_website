from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Myuser


class FormConnexion(forms.Form):
	login = forms.CharField(label="login", max_length=50)
	mdp = forms.CharField(label="mot de passe", widget=forms.PasswordInput)

	login.widget.attrs.update({"placeholder":"prénom.nom"})



class InscriptionForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajout de votre validateur à la liste existante
        self.fields['username'].validators.append(validation_usernanme)

    # Rendre le champ email obligatoire (par défaut dans le modèle User, il est optionnel)
    email = forms.EmailField(required=True, label="Adresse e-mail")


    class Meta(UserCreationForm.Meta):
        model = Myuser
        # On définit l'ordre d'affichage des champs dans le formulaire
        fields = ("username", "email")

        widgets = {'username': forms.TextInput(attrs={'placeholder': "prénom.nom"}),}

    def clean_email(self):
        """Optionnel : Empêche deux utilisateurs d'avoir la même adresse e-mail"""
        email = self.cleaned_data.get('email')
        if Myuser.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse e-mail est déjà utilisée.")
        return email


def validation_usernanme (value):
    if value.count('.') > 1:
        raise ValidationError("Votre nom d'utilisateur ne doit contenir qu'un seul point")
    if value.count('.') < 1:
        raise ValidationError('Merci de respecter la syntaxe "prénom.nom"')
