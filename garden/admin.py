"""Puutarhapäiväkirjan admin-konfiguraatio."""
from django.contrib import admin
from .models import PlantSpecies, MyGarden, GardenNote, Category


class CategoryAdmin(admin.ModelAdmin):
    """Admin-konfiguraatio Category-mallille."""
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)


class GardenNoteInline(admin.TabularInline):
    """Havainnot näkyvät viljelymerkinnän yhteydessä."""
    model = GardenNote
    extra = 1
    fields = ('paivamaara', 'havainto')


@admin.register(PlantSpecies)
class PlantSpeciesAdmin(admin.ModelAdmin):
    """Admin-konfiguraatio PlantSpecies-mallille."""
    list_display = ('nimi', 'lajike', 'kategoria', 'kasvupaikka', 'kylvo_alku_kk', 'kylvo_loppu_kk')
    list_filter = ('kategoria', 'kasvupaikka')
    search_fields = ('nimi', 'lajike', 'kategoria__name')
    fieldsets = (
        ('Perustiedot', {
            'fields': ('nimi', 'lajike', 'kategoria', 'kuvaus', 'kasvatusohje')
        }),
        ('Aikataulu', {
            'fields': (
                ('kylvo_alku_kk', 'kylvo_loppu_kk'),
                ('sato_alku_kk', 'sato_loppu_kk'),
                ('itamisaika_min_pv', 'itamisaika_max_pv'),
            )
        }),
        ('Kasvatustiedot', {
            'fields': ('korkeus_cm', 'kasvupaikka', 'siemenia_pakkauksessa')
        }),
        ('Nelson Garden', {
            'fields': ('nelson_garden_id', 'nelson_garden_url'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MyGarden)
class MyGardenAdmin(admin.ModelAdmin):
    """Admin-konfiguraatio MyGarden-mallille."""
    list_display = ('kasvilaji', 'kasvupaikka', 'tila', 'kylvopaiva', 'lisatty')
    list_filter = ('tila',)
    search_fields = ('kasvilaji__nimi', 'kasvupaikka')
    inlines = [GardenNoteInline]


@admin.register(GardenNote)
class GardenNoteAdmin(admin.ModelAdmin):
    """Admin-konfiguraatio GardenNote-mallille."""
    list_display = ('kasvi', 'paivamaara', 'havainto_lyhyt')
    list_filter = ('paivamaara',)
    search_fields = ('havainto',)

    def havainto_lyhyt(self, obj):
        """Palauttaa havainnosta lyhennetyn version listanäkymää varten."""
        return obj.havainto[:80] + '...' if len(obj.havainto) > 80 else obj.havainto
    havainto_lyhyt.short_description = 'Havainto'
