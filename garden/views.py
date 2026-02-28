"""Puutarhapäiväkirjan näkymät."""
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView
from django.urls import reverse
from .models import PlantSpecies, MyGarden, GardenNote
from .forms import MyGardenForm, TilaForm, GardenNoteForm, PlantSpeciesForm


# Kuukausien nimet suomeksi
KUUKAUDET = [
    '', 'Tammi', 'Helmi', 'Maalis', 'Huhti', 'Touko', 'Kesä',
    'Heinä', 'Elo', 'Syys', 'Loka', 'Marras', 'Joulu'
]


class EtusivuView(View):
    """Etusivu: kasvukalenteri (omat viljelyt) ja viljelylista."""

    def get(self, request):
        """Käsittelee GET-pyynnön ja palauttaa etusivun näkymän."""
        tama_kk = date.today().month
        omat_viljelyt = MyGarden.objects.exclude(tila='paattynyt').select_related('kasvilaji')

        # Kasvukalenteri: ryhmitellään omat viljelyt kategorioittain
        kategoriat_dict = {}
        for v in omat_viljelyt:
            laji = v.kasvilaji
            kat = laji.kategoria.name if laji.kategoria else ''
            if kat not in kategoriat_dict:
                kategoriat_dict[kat] = []

            kylvo_kk = set(laji.kylvo_kuukaudet())
            sato_kk = set(laji.sato_kuukaudet())

            # Kasvukuukaudet = kylvön jälkeen, ennen satoa
            if laji.kylvo_loppu_kk < laji.sato_alku_kk:
                kasvu_kk = set(range(laji.kylvo_loppu_kk + 1, laji.sato_alku_kk))
            else:
                kasvu_kk = set()

            kuukaudet = []
            for kk in range(1, 13):
                if kk in kylvo_kk:
                    tyyppi = 'kylvo'
                elif kk in kasvu_kk:
                    tyyppi = 'kasvu'
                elif kk in sato_kk:
                    tyyppi = 'sato'
                else:
                    tyyppi = ''
                kuukaudet.append({
                    'kk': kk,
                    'nimi': KUUKAUDET[kk],
                    'tyyppi': tyyppi,
                    'nykyinen': kk == tama_kk,
                })

            kategoriat_dict[kat].append({
                'viljely': v,
                'nimi': str(laji),
                'kuukaudet': kuukaudet,
            })

        kasvukalenteri = [
            {'kategoria': kat, 'kasvit': kasvit}
            for kat, kasvit in kategoriat_dict.items()
        ]

        kk_otsikot = [KUUKAUDET[kk] for kk in range(1, 13)]

        return render(request, 'garden/etusivu.html', {
            'omat_viljelyt': omat_viljelyt,
            'kasvukalenteri': kasvukalenteri,
            'kk_otsikot': kk_otsikot,
            'tama_kk': tama_kk,
        })


class KasvilistaView(ListView):
    """Kasvilista: kaikki lajit, suodatus kategorian mukaan."""
    model = PlantSpecies
    template_name = 'garden/kasvilista.html'
    context_object_name = 'kasvit'

    def get_queryset(self):
        """Palauttaa kasvilajit suodatettuna kategorialla (jos annettu)."""
        qs = super().get_queryset()
        kategoria = self.request.GET.get('kategoria')
        if kategoria:
            qs = qs.filter(kategoria__name=kategoria)
        return qs

    def get_context_data(self, **kwargs):
        """Lisää kategoriat ja valitun kategorian näkymän kontekstiin."""
        context = super().get_context_data(**kwargs)
        context['kategoriat'] = (
            PlantSpecies.objects.values_list('kategoria__name', flat=True)
            .distinct().order_by('kategoria__name')
        )
        context['valittu_kategoria'] = self.request.GET.get('kategoria', '')
        return context


class LisaaViljelyView(CreateView):
    """Lisää uusi viljelymerkintä."""
    model = MyGarden
    form_class = MyGardenForm
    template_name = 'garden/lisaa_viljely.html'

    def get_initial(self):
        """Asettaa alustavat arvot lomakkeelle (esim. kasvilaji url-parametrista)."""
        initial = super().get_initial()
        kasvilaji_id = self.request.GET.get('kasvilaji')
        if kasvilaji_id:
            initial['kasvilaji'] = kasvilaji_id
        return initial

    def get_success_url(self):
        """Palauttaa URL-osoitteen, johon ohjataan onnistuneen tallennuksen jälkeen."""
        return reverse('etusivu')


class LisaaKasvilajiView(CreateView):
    """Lisää uusi kasvilaji."""
    model = PlantSpecies
    form_class = PlantSpeciesForm
    template_name = 'garden/lisaa_kasvilaji.html'

    def get_success_url(self):
        """Palauttaa URL-osoitteen, johon ohjataan onnistuneen tallennuksen jälkeen."""
        return reverse('kasvilista')


class ViljelyDetailView(View):
    """Viljelymerkinnän yksityiskohdat + havainnot."""

    def get(self, request, pk):
        """Käsittelee GET-pyynnön viljelymerkinnän tiedoille."""
        viljely = get_object_or_404(
            MyGarden.objects.select_related('kasvilaji'), pk=pk
        )
        havainnot = viljely.havainnot.all()
        note_form = GardenNoteForm(initial={'paivamaara': date.today()})
        tila_form = TilaForm(instance=viljely)

        return render(request, 'garden/viljely_detail.html', {
            'viljely': viljely,
            'havainnot': havainnot,
            'note_form': note_form,
            'tila_form': tila_form,
        })

    def post(self, request, pk):
        """Käsittelee POST-pyynnön (tilan vaihto tai uusi havainto)."""
        viljely = get_object_or_404(MyGarden, pk=pk)

        # Tilan vaihto
        if 'vaihda_tila' in request.POST:
            tila_form = TilaForm(request.POST, instance=viljely)
            if tila_form.is_valid():
                tila_form.save()
            return redirect('viljely_detail', pk=pk)

        # Uusi havainto
        if 'lisaa_havainto' in request.POST:
            note_form = GardenNoteForm(request.POST)
            if note_form.is_valid():
                note = note_form.save(commit=False)
                note.kasvi = viljely
                note.save()
            return redirect('viljely_detail', pk=pk)

        return redirect('viljely_detail', pk=pk)


class VaihdaTilaView(View):
    """Tilan vaihto etusivulta (AJAX-tyylinen POST)."""

    def post(self, request, pk):
        """Käsittelee POST-pyynnön tilan vaihtamiseksi."""
        viljely = get_object_or_404(MyGarden, pk=pk)
        tila_form = TilaForm(request.POST, instance=viljely)
        if tila_form.is_valid():
            tila_form.save()
        return redirect('etusivu')
