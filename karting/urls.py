from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from karting.views import (
    index,
    RaceListView,
    KartListView,
    KartDetailView,
    RaceDetailView,
    RaceCreateView,
    RaceUpdateView,
    KartUpdateView,
    KartCreateView,
    KartDeleteView,
    RaceDeleteView,
    RegisterForRaceView,

)

app_name = "karting"

urlpatterns = [
    path("", index, name="index"),
    path("karts/", KartListView.as_view(), name="karts-list"),
    path("karts/create/", KartCreateView.as_view(), name="kart-create"),
    path("karts/<int:pk>/", KartDetailView.as_view(), name="kart-detail"),
    path("karts/<int:pk>/update/", KartUpdateView.as_view(), name="kart-update"),
    path("karts/<int:pk>/delete/", KartDeleteView.as_view(), name="kart-delete"),
    path("race/", RaceListView.as_view(), name="race-list"),
    path("race/create/", RaceCreateView.as_view(), name="race-create"),
    path("race/<int:pk>/", RaceDetailView.as_view(), name="race-detail"),
    path("race/<int:pk>/update/", RaceUpdateView.as_view(), name="race-update"),
    path("race/<int:pk>/delete/", RaceDeleteView.as_view(), name="race-delete"),
    path("race/<int:race_id>/register/", RegisterForRaceView.as_view(), name="register-for-race"),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
