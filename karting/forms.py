from django import forms

from karting.models import RaceParticipation, Kart


class RaceRegistrationForm(forms.ModelForm):
    class Meta:
        model = RaceParticipation
        fields = ["kart"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.race_category = kwargs.pop("race_category")
        super().__init__(*args, **kwargs)
        self.fields["kart"].queryset = Kart.objects.filter(category=self.race_category)