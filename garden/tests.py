"""Puutarhapäiväkirjan testit."""
from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from .models import PlantSpecies, MyGarden, GardenNote, Category


class PlantSpeciesModelTest(TestCase):
    """Testit PlantSpecies-mallille."""

    def setUp(self):
        self.kat_tomaatti = Category.objects.create(name='🍅 Tomaatti')
        self.kasvi = PlantSpecies.objects.create(
            nimi='Tomaatti', lajike='Sungold F1', kategoria=self.kat_tomaatti,
            kylvo_alku_kk=2, kylvo_loppu_kk=4,
            sato_alku_kk=7, sato_loppu_kk=9,
            itamisaika_min_pv=5, itamisaika_max_pv=15,
            korkeus_cm=150, kasvupaikka='aurinko',
        )

    def test_str(self):
        self.assertEqual(str(self.kasvi), "Tomaatti 'Sungold F1'")

    def test_str_ilman_lajiketta(self):
        kat_yrtit = Category.objects.create(name='🌿 Yrtit')
        kasvi = PlantSpecies.objects.create(
            nimi='Tilli', kategoria=kat_yrtit,
            kylvo_alku_kk=4, kylvo_loppu_kk=6,
            sato_alku_kk=6, sato_loppu_kk=9,
        )
        self.assertEqual(str(kasvi), 'Tilli')

    def test_kylvo_kuukaudet(self):
        self.assertEqual(self.kasvi.kylvo_kuukaudet(), [2, 3, 4])

    def test_sato_kuukaudet(self):
        self.assertEqual(self.kasvi.sato_kuukaudet(), [7, 8, 9])


class MyGardenModelTest(TestCase):
    """Testit MyGarden-mallille."""

    def setUp(self):
        self.kat_tomaatti = Category.objects.create(name='🍅 Tomaatti')
        self.kasvi = PlantSpecies.objects.create(
            nimi='Tomaatti', kategoria=self.kat_tomaatti,
            kylvo_alku_kk=2, kylvo_loppu_kk=4,
            sato_alku_kk=7, sato_loppu_kk=9,
        )
        self.viljely = MyGarden.objects.create(
            kasvilaji=self.kasvi, tila='kylvetty',
            kylvopaiva=date(2026, 3, 15),
        )

    def test_str(self):
        self.assertIn('Tomaatti', str(self.viljely))

    def test_arvioitu_sato(self):
        sato = self.viljely.arvioitu_sato()
        self.assertIsNotNone(sato)
        self.assertGreater(sato, self.viljely.kylvopaiva)

    def test_arvioitu_sato_ilman_kylvopaivaa(self):
        viljely = MyGarden.objects.create(kasvilaji=self.kasvi)
        self.assertIsNone(viljely.arvioitu_sato())


class GardenNoteModelTest(TestCase):
    """Testit GardenNote-mallille."""

    def setUp(self):
        kat_yrtit = Category.objects.create(name='🌿 Yrtit')
        kasvi = PlantSpecies.objects.create(
            nimi='Basilika', kategoria=kat_yrtit,
            kylvo_alku_kk=3, kylvo_loppu_kk=5,
            sato_alku_kk=6, sato_loppu_kk=9,
        )
        self.viljely = MyGarden.objects.create(kasvilaji=kasvi)
        self.note = GardenNote.objects.create(
            kasvi=self.viljely,
            paivamaara=date(2026, 4, 10),
            havainto='Ensimmäiset versot näkyvissä!',
        )

    def test_str(self):
        self.assertIn('Ensimmäiset versot', str(self.note))


class ViewsTest(TestCase):
    """Testit näkymille."""

    def setUp(self):
        self.client = Client()
        self.kat_tomaatti = Category.objects.create(name='🍅 Tomaatti')
        self.kasvi = PlantSpecies.objects.create(
            nimi='Tomaatti', kategoria=self.kat_tomaatti,
            kylvo_alku_kk=2, kylvo_loppu_kk=4,
            sato_alku_kk=7, sato_loppu_kk=9,
        )
        self.viljely = MyGarden.objects.create(
            kasvilaji=self.kasvi, tila='kylvetty',
            kylvopaiva=date(2026, 3, 15),
        )

    def test_etusivu(self):
        response = self.client.get(reverse('etusivu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Puutarhapäiväkirja')

    def test_kasvilista(self):
        response = self.client.get(reverse('kasvilista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tomaatti')

    def test_kasvilista_suodatus(self):
        response = self.client.get(reverse('kasvilista') + '?kategoria=🍅 Tomaatti')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tomaatti')

    def test_viljely_detail(self):
        response = self.client.get(reverse('viljely_detail', args=[self.viljely.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tomaatti')

    def test_lisaa_viljely(self):
        response = self.client.get(reverse('lisaa_viljely'))
        self.assertEqual(response.status_code, 200)

    def test_lisaa_viljely_post(self):
        response = self.client.post(reverse('lisaa_viljely'), {
            'kasvilaji': self.kasvi.pk,
            'tila': 'odottaa',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MyGarden.objects.count(), 2)

    def test_lisaa_kasvilaji(self):
        response = self.client.get(reverse('lisaa_kasvilaji'))
        self.assertEqual(response.status_code, 200)

    def test_vaihda_tila(self):
        response = self.client.post(
            reverse('vaihda_tila', args=[self.viljely.pk]),
            {'tila': 'itanyt'},
        )
        self.assertEqual(response.status_code, 302)
        self.viljely.refresh_from_db()
        self.assertEqual(self.viljely.tila, 'itanyt')

    def test_lisaa_havainto(self):
        response = self.client.post(
            reverse('viljely_detail', args=[self.viljely.pk]),
            {
                'lisaa_havainto': '1',
                'paivamaara': '2026-04-10',
                'havainto': 'Testi havainto',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(GardenNote.objects.count(), 1)
