from django.contrib.admin.sites import site
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from karting.models import Race, RaceCategory, Kart, RaceParticipation

User = get_user_model()

class AdminSiteTests(TestCase):

    def setUp(self):
        # create a test superuser
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password"
        )
        self.client.login(username="admin", password="password")

        # create some test data
        self.category = RaceCategory.objects.create(
            name="Junior",
            description="For kids",
            min_age=6,
            max_age=12
        )
        self.kart = Kart.objects.create(
            name="Fast Kart",
            category=self.category,
            speed=100,
            description="Very fast kart",
            available_quantity=5
        )
        self.race = Race.objects.create(
            name="Grand Prix",
            category=self.category,
            date="2024-01-01",
            max_participants=10
        )
        self.participation = RaceParticipation.objects.create(
            user=self.admin_user,
            race=self.race,
            kart=self.kart
        )

    def test_race_admin_list(self):
        url = reverse("admin:karting_race_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.race.name)

    def test_race_admin_add(self):
        url = reverse("admin:karting_race_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_race_admin_change(self):
        url = reverse("admin:karting_race_change", args=[self.race.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.race.name)

    def test_race_participation_admin_list(self):
        url = reverse("admin:karting_raceparticipation_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.participation.user.username)

    def test_race_category_admin_add(self):
        url = reverse("admin:karting_racecategory_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_kart_admin_list(self):
        url = reverse("admin:karting_kart_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.kart.name)

    def test_custom_user_admin_list(self):
        url = reverse("admin:karting_customuser_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.admin_user.username)

    def test_race_category_admin_change(self):
        url = reverse("admin:karting_racecategory_change", args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)

