from django.urls import path

from . import views

urlpatterns = [
    path("", views.EleveNotes.as_view(), name="EleveNotes"),
    path("colleur/", views.ColleurNotes.as_view(), name="colleurNotes"),
    path("colleur/nouvellecolle", views.NouvelleColle.as_view(), name="nouvelleColle"),
    path("colleur/modifiercolle/<int:colleId>", views.ModifierColle.as_view(), name="modifierColle"),
    path("colleur/supprimercolle/<int:colleId>", views.SupprimerColle.as_view(), name="supprimercolle"),
]