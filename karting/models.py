from django.conf import settings
from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager


RACE_CATEGORIES = {
    "pioner-n-mini": "Pioneer N Mini",
    "pioner-n": "Pioneer N",
    "national-junior": "National Junior",
    "junior": "Junior",
}


class CustomUserManager(UserManager):

    def create_superuser(
            self,
            username,
            email=None,
            password=None,
            **extra_fields
    ) -> AbstractUser:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        extra_fields.setdefault("age", 18)

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=False, blank=False)
    objects = CustomUserManager()


class RaceCategory(models.Model):
    name = models.CharField(
        max_length=100,
        choices=RACE_CATEGORIES.items(),
        unique=True)
    description = models.TextField()
    min_age = models.PositiveIntegerField()
    max_age = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Kart(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        RaceCategory,
        on_delete=models.CASCADE,
        related_name="karts"
    )
    speed = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class Race(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        RaceCategory,
        on_delete=models.CASCADE,
        related_name="races"
    )
    date = models.DateField()

    def __str__(self) -> str:
        return self.name

    def is_user_eligible(self, user) -> bool:
        return self.category.min_age <= user.age <= self.category.max_age


class RaceParticipation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="race_participations"
    )
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name="participations"
    )
    kart = models.ForeignKey(
        Kart,
        on_delete=models.CASCADE,
        related_name="race_participations"
    )
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.race.name} ({self.kart.name})"
