from datetime import date

from django.conf import settings
from django.db import models

from django.contrib.auth.models import AbstractUser

from karting.managers import CustomUserManager, RaceManager


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=False, blank=False)
    objects = CustomUserManager()

    @property
    def age(self) -> int | None:
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
                age -= 1
            return age
        return None


class RaceCategory(models.Model):
    name = models.CharField(
        max_length=100,
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
    available_quantity = models.PositiveIntegerField(default=0)

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
    max_participants = models.PositiveIntegerField()
    objects = RaceManager()

    def __str__(self) -> str:
        return self.name

    def is_user_eligible(self, user) -> bool:
        return self.category.min_age <= user.age <= self.category.max_age

    def is_full(self) -> bool:
        return self.participations.count() >= self.max_participants


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
