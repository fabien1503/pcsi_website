from django.urls import path

from . import views

urlpatterns = [
    path("", views.EleveDocuments.as_view(), name="EleveDocuments"),
    path("profdocument/", views.ProfDocuments.as_view(), name="profDocument"),
    path("consulter/<str:matiere>/<int:documentId>", views.ConsulterDoc.as_view(), name="consulterPDF"),
    path("consulter/<str:matiere>/correction/<int:correctionId>", views.ConsulterCorr.as_view(), name="consulterCorr"),
    path("supprimer/<int:documentId>", views.Supprimer.as_view(), name="SupprimerDoc"),
]