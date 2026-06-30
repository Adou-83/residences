from django.db import models


# =========================
# RESIDENCE
# =========================
class Residence(models.Model):

    nom = models.CharField(max_length=200)
    ville = models.CharField(max_length=100)
    description = models.TextField()
    prix_par_nuit = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    image = models.ImageField(upload_to='residences/', blank=True, null=True)

    def __str__(self):
        return self.nom


# =========================
# RESERVATION
# =========================
class Reservation(models.Model):

    residence = models.ForeignKey(
        Residence,
        on_delete=models.CASCADE,
        related_name='reservations'
    )

    nom_client = models.CharField(max_length=200)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)

    date_arrivee = models.DateField()
    date_depart = models.DateField()

    personnes = models.PositiveIntegerField()

    prix_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    confirme = models.BooleanField(default=False)

    date_reservation = models.DateTimeField(auto_now_add=True)

    # =========================
    # CALCUL PRIX
    # =========================
    def calculer_prix(self):
        nuits = (self.date_depart - self.date_arrivee).days
        return max(nuits, 1) * self.residence.prix_par_nuit

    # =========================
    # SAVE
    # =========================
    def save(self, *args, **kwargs):
        self.prix_total = self.calculer_prix()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom_client} - {self.residence.nom}"


# =========================
# IMAGES RESIDENCE
# =========================
class ImageResidence(models.Model):

    residence = models.ForeignKey(
        Residence,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='residences/')

    def __str__(self):
        return f"Image de {self.residence.nom}"