import os
import sys
import django

# Permet à Python de trouver le projet Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Configuration Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "residences.settings")
django.setup()


import cloudinary
import cloudinary.uploader

from core.models import Residence, ImageResidence


# ==========================
# CONFIGURATION CLOUDINARY
# ==========================

cloudinary.config(
    cloud_name="cvyyvsiw",
    api_key="992362496136332",
    api_secret="gulQFSpTCuSW"
)


print("=== Début migration Cloudinary ===")


# ==========================
# IMAGES PRINCIPALES
# ==========================

for residence in Residence.objects.all():

    if residence.image:

        try:
            print("Upload résidence :", residence.image.path)

            result = cloudinary.uploader.upload(
                residence.image.path,
                folder="residences"
            )

            residence.image = result["public_id"]
            residence.save(update_fields=["image"])

            print("OK :", result["secure_url"])


        except Exception as e:
            print("ERREUR résidence :", e)



# ==========================
# IMAGES SUPPLEMENTAIRES
# ==========================

for image in ImageResidence.objects.all():

    if image.image:

        try:
            print("Upload image :", image.image.path)

            result = cloudinary.uploader.upload(
                image.image.path,
                folder="residences"
            )


            image.image = result["public_id"]
            image.save(update_fields=["image"])


            print("OK :", result["secure_url"])


        except Exception as e:
            print("ERREUR image :", e)



print("=== Migration terminée ===")