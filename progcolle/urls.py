from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("profprog/modifier/<int:programmeId>", views.Modifier.as_view(), name="progModif"),
    path("profprog/supprimer/<int:programmeId>", views.Supprimer.as_view(), name="progSuppr"),
    path("profprog/", views.ProgProf.as_view(), name="progProf"),
]

