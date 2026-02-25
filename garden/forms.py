"""Puutarhapäiväkirjan lomakkeet."""
from django import forms
from .models import MyGarden, GardenNote, PlantSpecies


class MyGardenForm(forms.ModelForm):
    """Lomake uuden viljelymerkinnän luomiseen."""

    class Meta:
        model = MyGarden
        fields = ['kasvilaji', 'kasvupaikka', 'tila', 'kylvopaiva', 'muistiinpanot']
        widgets = {
            'kylvopaiva': forms.DateInput(attrs={'type': 'date'}),
            'muistiinpanot': forms.Textarea(attrs={'rows': 3}),
        }


class TilaForm(forms.ModelForm):
    """Lomake tilan vaihtamiseen."""

    class Meta:
        model = MyGarden
        fields = ['tila']


class GardenNoteForm(forms.ModelForm):
    """Lomake uuden havainnon lisäämiseen."""

    class Meta:
        model = GardenNote
        fields = ['paivamaara', 'havainto']
        widgets = {
            'paivamaara': forms.DateInput(attrs={'type': 'date'}),
            'havainto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Kirjoita havainto...'}),
        }


class PlantSpeciesForm(forms.ModelForm):
    """Lomake uuden kasvilajin lisäämiseen."""

    class Meta:
        model = PlantSpecies
        fields = [
            'nimi', 'lajike', 'kategoria', 'kuvaus', 'kasvatusohje',
            'kylvo_alku_kk', 'kylvo_loppu_kk', 'sato_alku_kk', 'sato_loppu_kk',
            'itamisaika_min_pv', 'itamisaika_max_pv', 'korkeus_cm',
            'kasvupaikka', 'siemenia_pakkauksessa',
        ]
        widgets = {
            'kuvaus': forms.Textarea(attrs={'rows': 3}),
            'kasvatusohje': forms.Textarea(attrs={'rows': 3}),
        }
