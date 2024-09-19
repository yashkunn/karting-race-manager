from django.urls import path

from karting.views import index

app_name = "karting"

urlpatterns = [
    path("", index, name="index"),
    ]