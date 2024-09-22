from django.urls import reverse
from django.test import TestCase
from karting.models import Kart, RaceCategory, CustomUser


class KartViewTests(TestCase):
    def setUp(self):
        self.category = RaceCategory.objects.create(
            name="Category 1",
            description="Description 1",
            min_age=18,
            max_age=35
        )
        self.kart = Kart.objects.create(
            name="Test Kart",
            category=self.category,
            speed=100,
            description="Fast Kart",
            available_quantity=10
        )

    def test_kart_list_view(self):
        response = self.client.get(reverse("karting:karts-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "karting/kart_list.html")
        self.assertContains(response, "Test Kart")

    def test_kart_create_view(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            password="password",
            date_of_birth="1990-01-01"
        )
        self.client.login(username="testuser", password="password")

        response = self.client.post(reverse("karting:kart-create"), {
            "name": "New Kart",
            "category": self.category.id,
            "speed": 100,
            "description": "Very fast kart",
            "available_quantity": 5
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Kart.objects.filter(name="New Kart").exists())

    def test_kart_update_view(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            password="password",
            date_of_birth="1990-01-01"
        )
        self.client.login(username="testuser", password="password")

        response = self.client.post(reverse("karting:kart-update", args=[self.kart.id]), {
            "name": "Updated Kart",
            "category": self.category.id,
            "speed": 20,
            "description": "Very slow kart",
            "available_quantity": 5
        })
        self.assertEqual(response.status_code, 302)
        self.kart.refresh_from_db()
        self.assertEqual(self.kart.name, "Updated Kart")

    def test_kart_delete_view(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            password="password",
            date_of_birth="1990-01-01"
        )
        self.client.login(username="testuser", password="password")

        response = self.client.post(reverse("karting:kart-delete", args=[self.kart.id]))
        self.assertEqual(response.status_code, 302)  # Redirects to kart list
        self.assertFalse(Kart.objects.filter(id=self.kart.id).exists())

    def test_kart_detail_view(self):
        response = self.client.get(reverse("karting:kart-detail", args=[self.kart.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "karting/kart-detail.html")
        self.assertContains(response, "Test Kart")
        self.assertContains(response, self.category.name)
