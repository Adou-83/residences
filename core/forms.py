from django import forms
from .models import Reservation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# =========================
# INSCRIPTION
# =========================

class InscriptionForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre adresse email'
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur"
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        })
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


# =========================
# RESERVATION
# =========================

class ReservationForm(forms.ModelForm):

    class Meta:

        model = Reservation

        fields = [
            'nom_client',
            'email',
            'telephone',
            'date_arrivee',
            'date_depart',
            'personnes'
        ]

        widgets = {

            'nom_client': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom complet'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre email'
            }),

            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone / WhatsApp'
            }),

            'date_arrivee': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'date_depart': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'personnes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Nombre de personnes'
            }),

        }

    # =========================
    # VALIDATION DATES
    # =========================

    def clean(self):

        cleaned_data = super().clean()

        date_arrivee = cleaned_data.get('date_arrivee')

        date_depart = cleaned_data.get('date_depart')

        if date_arrivee and date_depart:

            if date_depart <= date_arrivee:

                raise forms.ValidationError(
                    "La date de départ doit être après la date d'arrivée."
                )

        return cleaned_data