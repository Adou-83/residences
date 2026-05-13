from django.contrib import admin
from .models import Residence, Reservation, ImageResidence


admin.site.register(Residence)
admin.site.register(Reservation)
admin.site.register(ImageResidence)