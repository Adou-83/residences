from django.conf import settings

def global_settings(request):
    return {
        "WHATSAPP_NUMBER": settings.WHATSAPP_NUMBER
    }