from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from karting.views import index

app_name = "karting"

urlpatterns = [
    path("", index, name="index"),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)