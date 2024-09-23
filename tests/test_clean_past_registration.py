from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils import timezone
from karting.models import Race, RaceParticipation, Kart, RaceCategory
from django.test import TestCase


User = get_user_model()


class ClearRegistrationsViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="admin",
            password="adminpass",
            is_staff=True,
            date_of_birth="1990-01-01"
        )
        self.category = RaceCategory.objects.create(
            name="Category 1",
            description="Description 1",
            min_age=18,
            max_age=35
        )
        self.race_past = Race.objects.create(
            name="Past Race",
            category=self.category,
            max_participants=10,
            date=timezone.now() - timezone.timedelta(days=5)
        )
        self.race_future = Race.objects.create(
            name="Future Race",
            category=self.category,
            max_participants=10,
            date=timezone.now() + timezone.timedelta(days=5)
        )
        self.kart = Kart.objects.create(
            name="Kart 1",
            category=self.category,
            speed=100,
            description="Fast Kart",
            available_quantity=5
        )
        RaceParticipation.objects.create(
            race=self.race_past,
            user=self.user,
            kart=self.kart
        )
        RaceParticipation.objects.create(
            race=self.race_future,
            user=self.user,
            kart=self.kart
        )

    def test_clear_past_race_registrations(self):
        self.client.login(username="admin", password="adminpass")

        response = self.client.post(reverse("karting:clear-registrations"))
        self.assertRedirects(response, reverse("karting:race-list"))
        self.assertEqual(
            RaceParticipation.objects.filter(
                race=self.race_past
            ).count(),
            0
        )
        self.assertEqual(
            RaceParticipation.objects.filter(
                race=self.race_future
            ).count(),
            1
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "1 registrations have been deleted."
        )

    def test_no_registrations_deleted(self):
        RaceParticipation.objects.filter(race=self.race_past).delete()
        self.client.login(username="admin", password="adminpass")

        response = self.client.post(reverse("karting:clear-registrations"))
        self.assertRedirects(response, reverse("karting:race-list"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "No registrations have been deleted."
        )
