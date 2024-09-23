from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from karting.models import Race, RaceCategory, Kart, RaceParticipation

User = get_user_model()


class RegisterForRaceViewTests(TestCase):
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
            password="password",
            date_of_birth="1990-01-01"
        )

    def test_get_registration_form(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse(
                "karting:register-for-race",
                args=[self.race.id]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "karting/register_for_race.html")
        self.assertContains(response, "Register for Race 1")

    def test_register_for_race_success(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse(
                "karting:register-for-race",
                args=[self.race.id]),
            {"kart": self.kart.id, }
        )

        self.assertRedirects(
            response,
            reverse(
                "karting:race-detail",
                args=[self.race.id]
            )
        )
        self.assertTrue(
            RaceParticipation.objects.filter(
                user=self.user,
                race=self.race
            ).exists()
        )
        self.kart.refresh_from_db()
        self.assertEqual(self.kart.available_quantity, 4)

    def test_register_for_race_already_registered(self):
        self.client.login(username="testuser", password="password")
        RaceParticipation.objects.create(
            user=self.user,
            race=self.race,
            kart=self.kart
        )

        response = self.client.post(
            reverse(
                "karting:register-for-race",
                args=[self.race.id]
            ),
            {"kart": self.kart.id, }
        )

        self.assertRedirects(
            response,
            reverse(
                "karting:race-detail",
                args=[self.race.id]
            )
        )

        response = self.client.get(
            reverse(
                "karting:race-detail",
                args=[self.race.id]
            )
        )
        self.assertContains(
            response,
            "You are already registered for this race."
        )

    def test_register_for_race_full(self):
        self.client.login(username="testuser", password="password")

        for _ in range(self.race.max_participants):
            RaceParticipation.objects.create(
                user=self.user,
                race=self.race,
                kart=self.kart
            )

        response = self.client.post(
            reverse(
                "karting:register-for-race",
                args=[self.race.id]
            ),
            {"kart": self.kart.id, }
        )

        self.assertRedirects(
            response,
            reverse(
                "karting:race-detail",
                args=[self.race.id]
            )
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("This race is full." in str(msg) for msg in messages)
        )

        self.assertGreater(len(messages), 0)

    def test_no_registration_button_for_anonymous_user(self):
        self.client.logout()

        response = self.client.get(
            reverse(
                "karting:race-detail",
                args=[self.race.id]
            )
        )
        self.assertEqual(response.status_code, 200)

        expected_message = ("You must be "
                            "<a href='/accounts/login/'>logged</a> "
                            "in to register for the race."
                            )
        self.assertContains(response, expected_message, html=True)

        login_url = reverse("accounts:login")
        self.assertContains(response, f'href="{login_url}"')

        self.assertNotContains(response, "Sign Up for this Race")
