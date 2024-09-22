from django.contrib import messages
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from karting.forms import (
    RaceRegistrationForm,
    RaceSearchForm,
    KartSearchForm,
    RaceForm
)
from karting.models import Race, Kart, RaceParticipation


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
                Q(name__icontains=search_query)
                | Q(category__name__icontains=search_query)
            )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = RaceSearchForm(self.request.GET)
        return context


class RaceCreateView(generic.CreateView):
    model = Race
    form_class = RaceForm
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
        can_register = True
        is_registered = False

        if self.request.user.is_authenticated:
            is_eligible = race.is_user_eligible(self.request.user)
            is_registered = RaceParticipation.objects.filter(
                race=race,
                user=self.request.user
            ).exists()
            can_register = not race.is_full() and not is_registered

        context["is_eligible"] = is_eligible
        context["is_registered"] = is_registered
        context["can_register"] = can_register
        context["participants_count"] = race.participations.count()
        return context


class KartListView(generic.ListView):
    model = Kart
    template_name = "karting/kart_list.html"
    context_object_name = "karts"
    queryset = Kart.objects.select_related("category")
    paginate_by = 5

    def get_queryset(self):
        queryset = Kart.objects.select_related("category")
        form = KartSearchForm(self.request.GET)

        if form.is_valid():
            search_term = form.cleaned_data["search"]

            if search_term:
                queryset = queryset.filter(
                    Q(name__icontains=search_term)
                    | Q(category__name__icontains=search_term)
                )
        queryset = queryset.order_by("category__name")
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(KartListView, self).get_context_data(**kwargs)
        context["search_form"] = KartSearchForm(
            initial={
                "search": self.request.GET.get("search", ""),
            }
        )
        return context


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


class RegisterForRaceView(generic.View):

    def get_race_and_check_full(self, race_id):
        race = get_object_or_404(Race, id=race_id)
        is_full = race.participations.count() >= race.max_participants
        return race, is_full

    def user_already_registered(self, user, race):
        return RaceParticipation.objects.filter(user=user, race=race).exists()

    def handle_registration_errors(self, request, race):
        is_full = race.participations.count() >= race.max_participants
        if is_full:
            messages.error(request, "This race is full.")
            return True

        if self.user_already_registered(request.user, race):
            messages.error(
                request,
                "You are already registered for this race."
            )
            return True

        return False

    def get(self, request, race_id):
        race = self.get_race_and_check_full(race_id)[0]

        if self.handle_registration_errors(request, race):
            return redirect("karting:race-detail", pk=race.id)

        form = RaceRegistrationForm(
            user=request.user,
            race_category=race.category
        )
        return render(request, "karting/register_for_race.html", {
            "race": race,
            "username": request.user.username,
            "form": form,
        })

    def post(self, request, race_id):
        if not request.user.is_authenticated:
            messages.error(
                request,
                "You must be logged in to register for a race."
            )
            return redirect("accounts:login")

        race = self.get_race_and_check_full(race_id)[0]

        if self.handle_registration_errors(request, race):
            return redirect("karting:race-detail", pk=race.id)

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

            kart = form.cleaned_data["kart"]
            kart.available_quantity -= 1
            kart.save()
            return redirect("karting:race-detail", pk=race.id)

        return render(request, "karting/register_for_race.html", {
            "race": race,
            "username": request.user.username,
            "form": form,
        })


def unregister_from_race_view(request, race_id):
    if not request.user.is_authenticated:
        messages.error(
            request,
            "You must be logged in to unregister from a race."
        )
        return redirect("accounts:login")

    participation = get_object_or_404(
        RaceParticipation,
        race_id=race_id,
        user=request.user
    )

    kart = participation.kart
    kart.available_quantity += 1
    kart.save()

    participation.delete()

    messages.success(
        request,
        "You have successfully unregistered from the race."
    )
    return redirect("karting:race-detail", pk=race_id)


class ClearRegistrationsView(generic.View):
    def post(self, request):
        past_races = Race.objects.filter(date__lt=timezone.now().date())
        total_removed_count = 0

        for race in past_races:
            total_removed_count += race.clear_past_registrations()

        if total_removed_count > 0:
            messages.success(
                request,
                f"{total_removed_count} registrations have been deleted."
            )
        else:
            messages.info(request, "No registrations have been deleted.")

        return redirect("karting:race-list")
