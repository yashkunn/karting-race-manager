from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

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


class RaceListView(generic.ListView):
    model = Race
    template_name = "karting/race_list.html"
    queryset = Race.objects.select_related("category")
    paginate_by = 2


class RaceDetailView(generic.DetailView):
    model = Race
    queryset = Race.objects.select_related("category")
    template_name = "karting/race-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race = self.get_object()
        is_eligible = False

        if self.request.user.is_authenticated:
            is_eligible = race.is_user_eligible(self.request.user)

        context['is_eligible'] = is_eligible

        return context


class KartListView(generic.ListView):
    model = Kart
    template_name = "karting/kart_list.html"
    context_object_name = "karts"
    queryset = Kart.objects.select_related("category")
    paginate_by = 5


class KartDetailView(generic.DetailView):
    model = Kart
    queryset = Kart.objects.select_related("category")
    template_name = "karting/kart-detail.html"
