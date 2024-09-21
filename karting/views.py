from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from karting.forms import RaceRegistrationForm, RaceSearchForm
from karting.models import Race, Kart


def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""
    if request.user.is_staff:
        upcoming_races = Race.objects.order_by("date")[:3]
    else:
        upcoming_races = Race.objects.upcoming().order_by("date")[:3]
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
    paginate_by = 2

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Race.objects.select_related("category").order_by("date")
        else:
            queryset = Race.objects.upcoming().select_related("category")

        search_query = self.request.GET.get("search")

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(category__name__icontains=search_query)
            )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = RaceSearchForm(self.request.GET)
        return context


class RaceCreateView(generic.CreateView):
    model = Race
    fields = "__all__"
    success_url = reverse_lazy("karting:race-list")


class RaceUpdateView(generic.UpdateView):
    model = Race
    fields = "__all__"
    success_url = reverse_lazy("karting:race-list")


class RaceDeleteView(generic.DeleteView):
    model = Race
    success_url = reverse_lazy("karting:race-list")


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

        context["is_eligible"] = is_eligible

        return context


class KartListView(generic.ListView):
    model = Kart
    template_name = "karting/kart_list.html"
    context_object_name = "karts"
    queryset = Kart.objects.select_related("category")
    paginate_by = 5


class KartCreateView(generic.CreateView):
    model = Kart
    fields = "__all__"
    success_url = reverse_lazy("karting:karts-list")


class KartUpdateView(generic.UpdateView):
    model = Kart
    fields = "__all__"
    success_url = reverse_lazy("karting:karts-list")


class KartDeleteView(generic.DeleteView):
    model = Kart
    success_url = reverse_lazy("karting:karts-list")


class KartDetailView(generic.DetailView):
    model = Kart
    queryset = Kart.objects.select_related("category")
    template_name = "karting/kart-detail.html"


def register_for_race(request, race_id) -> HttpResponse:
    race = get_object_or_404(Race, id=race_id)

    if request.method == "POST":
        form = RaceRegistrationForm(
            request.POST,
            user=request.user,
            race_category=race.category
        )
        if form.is_valid():
            race_participation = form.save(commit=False)
            race_participation.user = request.user
            race_participation.race = race
            race_participation.save()
            return redirect("karting:race-detail", pk=race.id)
    else:
        form = RaceRegistrationForm(user=request.user, race_category=race.category)

    return render(request, "karting/register_for_race.html", {
        "race": race,
        "username": request.user.username,
        "form": form,
    })


