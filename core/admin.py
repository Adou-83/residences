from django.contrib import admin
from .models import Residence, Reservation, ImageResidence


# =========================
# GALERIE INLINE
# =========================
class ImageResidenceInline(admin.TabularInline):
    model = ImageResidence
    extra = 3


# =========================
# ADMIN RESIDENCE
# =========================
class ResidenceAdmin(admin.ModelAdmin):
    inlines = [ImageResidenceInline]


# =========================
# REGISTER
# =========================
admin.site.register(Residence, ResidenceAdmin)
admin.site.register(Reservation)