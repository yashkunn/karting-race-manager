from django import forms

from karting.models import RaceParticipation, Kart, Race


class RaceForm(forms.ModelForm):
    class Meta:
        model = Race
        fields = ["name", "category", "date", "max_participants"]
        widgets = {
            "date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
        }


class RaceRegistrationForm(forms.ModelForm):
    class Meta:
        model = RaceParticipation
        fields = ["kart"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.race_category = kwargs.pop("race_category")
        super().__init__(*args, **kwargs)

        self.fields["kart"].queryset = Kart.objects.filter(
            category=self.race_category,
            available_quantity__gt=0
        )


class RaceSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search by Name or Category",
            "class": "form-control",
        }),
    )


class KartSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search by Name or Category",
            "class": "form-control",
        }),
    )
