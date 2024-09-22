from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from karting.models import Race, Kart, RaceParticipation, RaceCategory

User = get_user_model()


class UnregisterFromRaceViewTests(TestCase):

    def setUp(self):
        self.category = RaceCategory.objects.create(
            name="Category 1",
            description="Description 1",
            min_age=18,
            max_age=35
        )
        self.kart = Kart.objects.create(
            name="Kart 1",
            category=self.category,
            speed=100,
            description="Fast Kart",
            available_quantity=5
        )
        self.race = Race.objects.create(
            name="Race 1",
            category=self.category,
            date="2024-10-01",
            max_participants=10
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            date_of_birth="1990-01-01"
        )
        self.participation = RaceParticipation.objects.create(
            race=self.race,
            user=self.user,
            kart=self.kart
        )

    def test_successful_unregister(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse(
            "karting:unregister-from-race",
            args=[self.race.id])
        )
        self.assertRedirects(response, reverse(
            "karting:race-detail",
            args=[self.race.id])
                             )
        self.assertEqual(RaceParticipation.objects.count(), 0)

    def test_kart_quantity_increased_after_unregister(self):
        self.client.login(username="testuser", password="testpass")
        initial_quantity = self.kart.available_quantity
        self.client.get(reverse("karting:unregister-from-race", args=[self.race.id]))
        self.kart.refresh_from_db()
        self.assertEqual(self.kart.available_quantity, initial_quantity + 1)
