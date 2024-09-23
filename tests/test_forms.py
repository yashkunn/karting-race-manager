from django.test import TestCase
from karting.models import (
    Race,
    RaceCategory,
    Kart,
    CustomUser,
    RaceParticipation
)
from karting.forms import (
    RaceForm,
    RaceRegistrationForm,
    RaceSearchForm,
    KartSearchForm
)


class RaceFormTest(TestCase):
    def setUp(self):
        self.category = RaceCategory.objects.create(
            name="Category 1",
            description="Description",
            min_age=10,
            max_age=20
        )

    def test_valid_form(self):
        form_data = {
            "name": "Race 1",
            "category": self.category.id,
            "date": "2023-09-22",
            "max_participants": 10
        }
        form = RaceForm(data=form_data)
        self.assertTrue(form.is_valid())
        race = form.save()
        self.assertEqual(race.name, "Race 1")

    def test_invalid_form(self):
        form_data = {
            "name": "",
            "category": self.category.id,
            "date": "2023-09-22",
            "max_participants": 10
        }
        form = RaceForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class RaceRegistrationFormTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user1",
            password="password",
            date_of_birth="2000-01-01"
        )
        self.category = RaceCategory.objects.create(
            name="Category 1",
            description="Description",
            min_age=10,
            max_age=20
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
            date="2023-09-22",
            max_participants=10
        )

    def test_valid_registration_form(self):
        form_data = {
            "kart": self.kart.id
        }
        form = RaceRegistrationForm(
            data=form_data,
            user=self.user,
            race_category=self.category
        )
        self.assertTrue(form.is_valid())
        participation = form.save(commit=False)
        participation.user = self.user
        participation.race = self.race
        participation.save()
        self.assertEqual(RaceParticipation.objects.count(), 1)

    def test_invalid_registration_form(self):
        form_data = {
            "kart": ""
        }
        form = RaceRegistrationForm(
            data=form_data,
            user=self.user,
            race_category=self.category
        )
        self.assertFalse(form.is_valid())
        self.assertIn("kart", form.errors)


class RaceSearchFormTest(TestCase):
    def test_valid_search_form(self):
        form = RaceSearchForm(data={"search": "Race 1"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["search"], "Race 1")

    def test_empty_search_form(self):
        form = RaceSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["search"], "")


class KartSearchFormTest(TestCase):
    def test_valid_kart_search_form(self):
        form = KartSearchForm(data={"search": "Kart 1"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["search"], "Kart 1")

    def test_empty_kart_search_form(self):
        form = KartSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["search"], "")
