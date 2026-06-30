from django.urls import path
from . import views

urlpatterns = [

    # ================= FRONT =================
    path('', views.accueil, name='accueil'),
    path('residences/', views.residences, name='residences'),
    path('residences/<int:id>/', views.residence_detail, name='residence_detail'),
    path('contact/', views.contact, name='contact'),

    # ================= AUTH =================
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('mes-reservations/', views.mes_reservations, name='mes_reservations'),

    # ================= BACKOFFICE =================
    path('backoffice/dashboard/', views.dashboard, name='dashboard'),
    path('backoffice/reservations/', views.reservations_admin, name='reservations_admin'),

    path(
        'backoffice/reservations/confirmer/<int:id>/',
        views.confirmer_reservation,
        name='confirmer_reservation'
    ),

    path(
        'backoffice/reservations/annuler/<int:id>/',
        views.annuler_reservation,
        name='annuler_reservation'
    ),
]