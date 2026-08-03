from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from django.db.models import Count, Sum, Q
from .models import Residence, Reservation
from .forms import ReservationForm, InscriptionForm


# =========================
# ACCUEIL
# =========================
def accueil(request):
    return render(request, 'core/accueil.html', {
        'residences': Residence.objects.filter(disponible=True)
    })


# =========================
# RESIDENCES
# =========================
def residences(request):
    return render(request, 'core/residences.html', {
        'residences': Residence.objects.filter(disponible=True)
    })


# =========================
# DETAIL RESIDENCE + RESERVATION
# =========================
def residence_detail(request, id):
    
    residence = get_object_or_404(Residence, id=id)
    reservations = Reservation.objects.filter(residence=residence)

    dates_reservees = [
        {
            "from": r.date_arrivee.strftime("%Y-%m-%d"),
            "to": r.date_depart.strftime("%Y-%m-%d")
        }
        for r in reservations
    ]

    form = ReservationForm()

    if request.method == "POST":

        print("=" * 60)
        print("POST reçu pour la résidence :", residence.nom)

        form = ReservationForm(request.POST)

        print("Données POST :", request.POST)

        if form.is_valid():

            print("✅ Formulaire valide")

            date_arrivee = form.cleaned_data["date_arrivee"]
            date_depart = form.cleaned_data["date_depart"]

            conflit = Reservation.objects.filter(
                residence=residence,
                date_arrivee__lt=date_depart,
                date_depart__gt=date_arrivee
            ).exists()

            print("Conflit :", conflit)

            if conflit:
                messages.error(request, "❌ Ces dates sont déjà réservées.")
                return redirect("residence_detail", id=residence.id)

            reservation = form.save(commit=False)
            reservation.residence = residence

            if request.user.is_authenticated:
                reservation.email = request.user.email

            reservation.save()

            print("✅ Réservation enregistrée")
            print("ID :", reservation.id)

            send_mail(
                subject="Nouvelle réservation",
                message=f"""
Résidence : {residence.nom}
Ville : {residence.ville}

Client : {reservation.nom_client}
Téléphone : {reservation.telephone}
Email : {reservation.email}

Arrivée : {reservation.date_arrivee}
Départ : {reservation.date_depart}

Prix total : {reservation.prix_total} FCFA
""",
                from_email="system@residences.com",
                recipient_list=["proprietaire@gmail.com"],
                fail_silently=True,
            )

            messages.success(request, "✅ Réservation enregistrée avec succès")
            return redirect("residence_detail", id=residence.id)

        else:
            print("❌ Formulaire invalide")
            print(form.errors)

    return render(request, "core/residence_detail.html", {
        "residence": residence,
        "form": form,
        "reservations": reservations,
        "dates_reservees": dates_reservees,
    })
# =========================
# MES RESERVATIONS
# =========================
@login_required
def mes_reservations(request):

    reservations = Reservation.objects.filter(
        email=request.user.email
    ).order_by('-date_reservation')

    total = sum(r.prix_total or 0 for r in reservations)

    return render(request, 'core/mes_reservations.html', {
        'reservations': reservations,
        'total_reservations': reservations.count(),
        'total_depense': total
    })


# =========================
# ADMIN RESERVATIONS
# =========================
@staff_member_required
def reservations_admin(request):

    reservations = Reservation.objects.all().order_by('-date_reservation')

    return render(request, 'core/reservations_admin.html', {
        'reservations': reservations
    })

@staff_member_required
def confirmer_reservation(request, id):

    reservation = get_object_or_404(
        Reservation,
        id=id
    )

    reservation.confirme = True
    reservation.save()


    # =========================
    # NOTIFICATION CLIENT
    # =========================

    if reservation.email:

        send_mail(

            subject="Confirmation de votre réservation - Résidences LAMCY",

            message=f"""
Bonjour {reservation.nom_client},

Votre réservation est maintenant confirmée.

🏠 Résidence :
{reservation.residence.nom}

📍 Ville :
{reservation.residence.ville}

📅 Arrivée :
{reservation.date_arrivee}

📅 Départ :
{reservation.date_depart}

👥 Personnes :
{reservation.personnes}

💰 Montant :
{reservation.prix_total} FCFA


Merci pour votre confiance.

Résidences LAMCY
📞 2250778485274
""",

            from_email="contact@residences.com",

            recipient_list=[
                reservation.email
            ],

            fail_silently=True,
        )


    messages.success(
        request,
        "Réservation confirmée et notification envoyée"
    )

    return redirect(
        'reservations_admin'
    )
    
    
@staff_member_required
def annuler_reservation(request, id):

    reservation = get_object_or_404(Reservation, id=id)
    reservation.delete()

    messages.success(request, "Réservation annulée")
    return redirect('reservations_admin')


# =========================
# CONTACT
# =========================
def contact(request):
    return render(request, 'core/contact.html')


# =========================
# INSCRIPTION
# =========================
def inscription(request):

    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accueil')
    else:
        form = InscriptionForm()

    return render(request, 'core/inscription.html', {'form': form})


# =========================
# CONNEXION
# =========================
def connexion(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('dashboard' if user.is_staff else 'accueil')

    else:
        form = AuthenticationForm()

    return render(request, 'core/connexion.html', {'form': form})


# =========================
# DECONNEXION
# =========================
def deconnexion(request):
    logout(request)
    return redirect('accueil')


# =========================
# DASHBOARD
# =========================
 # =========================
# DASHBOARD
# =========================

@staff_member_required
def dashboard(request):

    reservations = Reservation.objects.all()
    residences = Residence.objects.all()


    # =========================
    # STATISTIQUES GENERALES
    # =========================

    total_reservations = reservations.count()

    total_confirmees = reservations.filter(
        confirme=True
    ).count()

    total_attente = reservations.filter(
        confirme=False
    ).count()


    revenus = sum(
        r.prix_total or 0
        for r in reservations
    )



    # =========================
    # PERFORMANCE RESIDENCES
    # =========================

    performance_residences = []


    for residence in residences:

        reservations_residence = Reservation.objects.filter(
            residence=residence
        )

        performance_residences.append({

            "nom": residence.nom,

            "ville": residence.ville,

            "nombre_reservations":
                reservations_residence.count(),

            "confirmees":
                reservations_residence.filter(
                    confirme=True
                ).count(),

            "revenus":
                sum(
                    r.prix_total or 0
                    for r in reservations_residence
                )

        })



    # =========================
    # RESERVATIONS PAR MOIS
    # =========================

    stats = (
        reservations
        .annotate(
            month=ExtractMonth('date_reservation')
        )
        .values('month')
        .annotate(
            total=Count('id')
        )
        .order_by('month')
    )


    noms_mois = {

        1:"Jan",
        2:"Fév",
        3:"Mar",
        4:"Avr",
        5:"Mai",
        6:"Juin",
        7:"Juil",
        8:"Août",
        9:"Sep",
        10:"Oct",
        11:"Nov",
        12:"Déc"

    }


    mois = [
        noms_mois.get(
            s['month']
        )
        for s in stats
    ]


    totaux = [
        s['total']
        for s in stats
    ]



    return render(
        request,
        'core/dashboard.html',
        {

            'total_residences':
                residences.count(),

            'total_reservations':
                total_reservations,

            'total_confirmees':
                total_confirmees,

            'total_attente':
                total_attente,

            'revenus':
                revenus,


            'performance_residences':
                performance_residences,


            'mois':
                mois,

            'totaux':
                totaux,


            'last_reservations':
                reservations.order_by(
                    '-date_reservation'
                )[:5],

        }
    )
    
    
 


@staff_member_required
def clients(request):

    clients = (
        Reservation.objects
        .values(
            'nom_client',
            'email',
            'telephone'
        )
        .annotate(
            nombre_reservations=Count('id'),
            total_depense=Sum('prix_total')
        )
        .order_by('-nombre_reservations')
    )


    return render(request, 'core/clients.html', {
        'clients': clients
    })