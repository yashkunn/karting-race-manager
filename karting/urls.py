from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from karting.views import (
    index,
    RaceListView,
    KartListView,
    KartDetailView,
    RaceDetailView
)

app_name = "karting"

urlpatterns = [
    path("", index, name="index"),
    path("race/", RaceListView.as_view(), name="race-list"),
    path("karts/", KartListView.as_view(), name="karts-list"),
    path("karts/<int:pk>/", KartDetailView.as_view(), name="kart-detail"),
    path("race/<int:pk>/", RaceDetailView.as_view(), name="race-detail"),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)