
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class GenerateurTokenActivation(PasswordResetTokenGenerator):
    
    def _make_hash_value(self, user, timestamp):
        # Le jeton expire automatiquement si le statut d'activité change
        return str(user.pk) + str(timestamp) + str(user.is_active)

generateur_token = GenerateurTokenActivation()
