from django.urls import path

from . import views
from django.contrib.auth import views as viewsContrib

urlpatterns = [
    path("", views.Index.as_view(), name="indexConnexion"),
    path("inscription/", views.Inscription.as_view(), name="inscription"),
    path('inscription/attente/', views.Attente.as_view(), name='activation_attente'),
    path('activer/<str:uidb64>/<str:token>/', views.activer_compte, name='activer'),
    path("deconnexion/", views.Deconnexion.as_view(), name="deconnexion"),
    path("annuaire/",views.Annuaire.as_view(), name="annuaire"),
    path("password_reset/", viewsContrib.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", viewsContrib.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", viewsContrib.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", viewsContrib.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    ]