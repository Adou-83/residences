import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Residence, Reservation
from django.contrib import messages
from .forms import ReservationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import InscriptionForm
from django.core.mail import send_mail

def accueil(request):
    return render(request, 'core/accueil.html')

def residences(request):
    toutes_residences = Residence.objects.all()
    return render(request, 'core/residences.html', {'residences': toutes_residences})

def residence_detail(request, id):
    
    residence = get_object_or_404(Residence, id=id)

    reservations = Reservation.objects.filter(residence=residence)

    # dates réservées pour le calendrier
    dates_reservees = []
    for r in reservations:
        dates_reservees.append({
            "start": r.date_arrivee.strftime("%Y-%m-%d"),
            "end": r.date_depart.strftime("%Y-%m-%d")
        })

    if request.method == 'POST':

        form = ReservationForm(request.POST)

        if form.is_valid():

            date_arrivee = form.cleaned_data['date_arrivee']
            date_depart = form.cleaned_data['date_depart']

            conflits = Reservation.objects.filter(
                residence=residence,
                date_arrivee__lt=date_depart,
                date_depart__gt=date_arrivee
            )

            if conflits.exists():
                messages.error(request, "Ces dates sont déjà réservées.")
            else:
                reservation = form.save(commit=False)
                reservation.residence = residence
                reservation.save()

                messages.success(request, "Réservation enregistrée")
                return redirect('residence_detail', id=residence.id)

    else:
        form = ReservationForm()
        
        residence = get_object_or_404(Residence, id=id)

    reservations = Reservation.objects.filter(residence=residence)

    dates_reservees = []

    for r in reservations:
        dates_reservees.append({
            "from": r.date_arrivee.strftime("%Y-%m-%d"),
            "to": r.date_depart.strftime("%Y-%m-%d")
        })

    return render(request, 'core/residence_detail.html', {
    'residence': residence,
    'form': form,
    'reservations': reservations,
    'dates_reservees': dates_reservees
})

@login_required
def reservations_admin(request):
    """Voir toutes les réservations"""
    toutes_reservations = Reservation.objects.all().order_by('-date_reservation')
    return render(request, 'core/reservations_admin.html', {'reservations': toutes_reservations})


@login_required
def confirmer_reservation(request, id):
    """Confirmer une réservation"""
    reservation = get_object_or_404(Reservation, id=id)
    reservation.confirme = True
    reservation.save()
    messages.success(request, f"Réservation de {reservation.nom_client} confirmée.")
    return redirect('reservations_admin')


@login_required
def annuler_reservation(request, id):
    """Annuler une réservation"""
    reservation = get_object_or_404(Reservation, id=id)
    reservation.delete()
    messages.success(request, f"Réservation de {reservation.nom_client} annulée.")
    return redirect('reservations_admin')

def contact(request):
    return render(request, 'core/contact.html')

# Inscription
def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # connexion automatique après inscription
            return redirect('accueil')
    else:
        form = InscriptionForm()
    return render(request, 'core/inscription.html', {'form': form})


# Connexion
def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accueil')
    else:
        form = AuthenticationForm()
    return render(request, 'core/connexion.html', {'form': form})


# Déconnexion
def deconnexion(request):
    logout(request)
    return redirect('accueil')