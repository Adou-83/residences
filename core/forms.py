from django import forms
from .models import Reservation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']









class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['nom_client', 'email', 'telephone', 'date_arrivee', 'date_depart', 'personnes']
        widgets = {
            'date_arrivee': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_depart': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nom_client': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'personnes': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }