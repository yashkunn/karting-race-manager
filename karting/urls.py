from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from karting.views import index, RaceListView, KartListView

app_name = "karting"

urlpatterns = [
    path("", index, name="index"),
    path("race/", RaceListView.as_view(), name="race-list"),
    path("kart/", KartListView.as_view(), name="kart-list"),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)