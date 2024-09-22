from django.test import TestCase
from django.utils import timezone
from karting.models import CustomUser, RaceCategory, Kart, Race, RaceParticipation


class CustomUserTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpassword",
            date_of_birth=timezone.datetime(2000, 1, 1).date()
        )

    def test_user_age(self):
        expected_age = timezone.now().year - 2000
        self.assertEqual(self.user.age, expected_age)

    def test_user_age_not_set(self):
        user_with_dob = CustomUser.objects.create_user(
            username="user2",
            password="password",
            date_of_birth=timezone.datetime(2000, 1, 1).date()
        )
        self.assertIsNotNone(user_with_dob.age)


class RaceCategoryTests(TestCase):

    def setUp(self):
        self.category = RaceCategory.objects.create(
            name="Junior",
            description="For kids",
            min_age=6,
            max_age=12
        )

    def test_str_representation(self):
        self.assertEqual(str(self.category), "Junior")

    def test_category_creation(self):
        self.assertEqual(RaceCategory.objects.count(), 1)


class KartTests(TestCase):

    def setUp(self):
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

    def test_str_representation(self):
        self.assertEqual(str(self.kart), "Fast Kart")

    def test_kart_creation(self):
        self.assertEqual(Kart.objects.count(), 1)


class RaceTests(TestCase):

    def setUp(self):
        self.category = RaceCategory.objects.create(
            name="Junior",
            description="For kids",
            min_age=6,
            max_age=12
        )
        self.race = Race.objects.create(
            name="Grand Prix",
            category=self.category,
            date="2024-01-01",
            max_participants=10
        )

    def test_str_representation(self):
        self.assertEqual(str(self.race), "Grand Prix")

    def test_is_user_eligible(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            password="testpassword",
            date_of_birth=timezone.datetime(2015, 1, 1).date()
        )
        self.assertTrue(self.race.is_user_eligible(user))

    def test_is_full(self):
        self.assertFalse(self.race.is_full())

    def test_clear_past_registrations(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            password="testpassword",
            date_of_birth="2000-01-01"
        )
        kart = Kart.objects.create(
            name="Fast Kart",
            category=self.category,
            speed=100,
            description="Very fast kart",
            available_quantity=5
        )
        participation = RaceParticipation.objects.create(
            user=user,
            race=self.race,
            kart=kart
        )

        self.race.date = timezone.now().date() - timezone.timedelta(days=1)
        self.race.save()

        count_removed = self.race.clear_past_registrations()
        self.assertEqual(count_removed, 1)
        self.assertEqual(RaceParticipation.objects.count(), 0)


class RaceParticipationTests(TestCase):

    def setUp(self):
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
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpassword",
            date_of_birth="2000-01-01"
        )
        self.race = Race.objects.create(
            name="Grand Prix",
            category=self.category,
            date="2024-01-01",
            max_participants=10
        )
        self.participation = RaceParticipation.objects.create(
            user=self.user,
            race=self.race,
            kart=self.kart
        )

    def test_str_representation(self):
        self.assertEqual(str(self.participation), "testuser - Grand Prix (Fast Kart)")
