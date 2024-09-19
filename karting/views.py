from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from karting.models import Race, Kart


def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""

    upcoming_races = Race.objects.order_by("date")[:3]
    popular_karts = Kart.objects.order_by("-speed")[:3]
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "upcoming_races": upcoming_races,
        "popular_karts": popular_karts,
        "num_visits": num_visits + 1,
    }

    return render(request, "karting/index.html", context=context)
