from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Race, 
    RaceCategory, 
    Kart, 
    CustomUser, 
    RaceParticipation
)


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "date")
    list_filter = ("category",)
    search_fields = ("category__name", "name")


@admin.register(RaceCategory)
class RaceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "min_age", "max_age")
    search_fields = ("name",)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("age",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("date_of_birth",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "date_of_birth",
                        "email",
                    )
                },
            ),
        )
    )


@admin.register(RaceParticipation)
class RaceParticipationAdmin(admin.ModelAdmin):
    list_display = ("user", "race", "kart", "date_registered")
    list_filter = ("race", "kart", "date_registered")
    search_fields = ("user__username", "race__name", "kart__name")
    date_hierarchy = "date_registered"


@admin.register(Kart)
class KartAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "speed")
    list_filter = ("category", "speed")
    search_fields = ("name", "category__name")
    