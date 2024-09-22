from datetime import date, timedelta

from django.urls import reverse
from django.test import TestCase
from karting.models import Race, RaceCategory, CustomUser


class RaceListViewTests(TestCase):
    def setUp(self):
        self.category = RaceCategory.objects.create(
            name="Category 1", 
            description="Description 1", 
            min_age=18, 
            max_age=35
        )
        self.race1 = Race.objects.create(
            name="Race 1", 
            category=self.category, 
            date="2024-10-01", 
            max_participants=10
        )
        self.race2 = Race.objects.create(
            name="Race 2", 
            category=self.category, 
            date="2024-09-01",
            max_participants=5)

    def test_race_list_view_with_authenticated_user(self):
        user = CustomUser.objects.create_user(
            username="testuser", 
            password="password", 
            date_of_birth="1990-01-01"
        )
        self.client.login(username="testuser", password="password")

        response = self.client.get(reverse("karting:race-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "karting/race_list.html")
        self.assertContains(response, "Race 1")
        self.assertNotContains(response, "Race 2")

    def test_race_list_view_with_staff_user(self):
        staff_user = CustomUser.objects.create_user(
            username="staffuser", 
            password="password", 
            is_staff=True, 
            date_of_birth="1990-01-01"
        )
        self.client.login(username="staffuser", password="password")

        response = self.client.get(reverse("karting:race-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "karting/race_list.html")
        self.assertContains(response, "Race 1")
        self.assertContains(response, "Race 2")

    def test_race_list_view_search_functionality(self):
        user = CustomUser.objects.create_user(
            username="testuser", 
            password="password", 
            date_of_birth="1990-01-01"
        )
        self.client.login(username="testuser", password="password")

        response = self.client.get(reverse("karting:race-list") + "?search=Race 1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Race 1")
        self.assertNotContains(response, "Race 2")

    def test_race_list_view_no_races(self):
        Race.objects.all().delete()

        response = self.client.get(reverse("karting:race-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "karting/race_list.html")
        self.assertContains(response, "There are no upcoming races in the schedule.")


class RaceViewTests(TestCase):
    def setUp(self):
        self.category = RaceCategory.objects.create(
            name="Category 1",
            description="Description 1",
            min_age=18,
            max_age=35
        )
        self.race = Race.objects.create(
            name="Test Race",
            category=self.category,
            date=date.today() + timedelta(days=1),
            max_participants=10
        )

    def test_create_race_view(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            password="password",
            date_of_birth="1990-01-01"
        )
        self.client.login(username="testuser", password="password")

        response = self.client.post(reverse("karting:race-create"), {
            "name": "New Race",
            "category": self.category.id,
            "date": date.today() + timedelta(days=2),
            "max_participants": 5
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Race.objects.filter(name="New Race").exists())

    def test_update_race_view(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            password="password",
            date_of_birth="1990-01-01"
        )
        self.client.login(username="testuser", password="password")

        response = self.client.post(reverse("karting:race-update", args=[self.race.id]), {
            "name": "Updated Race",
            "category": self.category.id,
            "date": date.today() + timedelta(days=2),
            "max_participants": 5
        })
        self.assertEqual(response.status_code, 302)
        self.race.refresh_from_db()
        self.assertEqual(self.race.name, "Updated Race")

    def test_delete_race_view(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            password="password",
            date_of_birth="1990-01-01"
        )
        self.client.login(username="testuser", password="password")

        response = self.client.post(reverse("karting:race-delete", args=[self.race.id]))
        self.assertEqual(response.status_code, 302)  # Redirects to race list
        self.assertFalse(Race.objects.filter(id=self.race.id).exists())

    def test_race_detail_view(self):
        response = self.client.get(reverse("karting:race-detail", args=[self.race.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "karting/race-detail.html")
        self.assertContains(response, "Test Race")
        self.assertContains(response, self.category.name)
