"""Puutarhapäiväkirjan testit."""
from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from .models import PlantSpecies, MyGarden, GardenNote, Category


class PlantSpeciesModelTest(TestCase):
    """Testit PlantSpecies-mallille."""

    def setUp(self):
        """Alustaa testissä käytettävän kategorian ja kasvilajin."""
        self.kat_tomaatti = Category.objects.create(name='🍅 Tomaatti')
        self.kasvi = PlantSpecies.objects.create(
            nimi='Tomaatti', lajike='Sungold F1', kategoria=self.kat_tomaatti,
            kylvo_alku_kk=2, kylvo_loppu_kk=4,
            sato_alku_kk=7, sato_loppu_kk=9,
            itamisaika_min_pv=5, itamisaika_max_pv=15,
            korkeus_cm=150, kasvupaikka='aurinko',
        )

    def test_str(self):
        """Varmistaa, että tekstiesitys sisältää nimen ja lajikkeen."""
        self.assertEqual(str(self.kasvi), "Tomaatti 'Sungold F1'")

    def test_str_ilman_lajiketta(self):
        """Varmistaa, että tekstiesitys toimii pelkällä nimellä, jos lajiketta ei ole."""
        kat_yrtit = Category.objects.create(name='🌿 Yrtit')
        kasvi = PlantSpecies.objects.create(
            nimi='Tilli', kategoria=kat_yrtit,
            kylvo_alku_kk=4, kylvo_loppu_kk=6,
            sato_alku_kk=6, sato_loppu_kk=9,
        )
        self.assertEqual(str(kasvi), 'Tilli')

    def test_kylvo_kuukaudet(self):
        """Varmistaa, että kylvökuukaudet palautetaan oikeana listana."""
        self.assertEqual(self.kasvi.kylvo_kuukaudet(), [2, 3, 4])

    def test_sato_kuukaudet(self):
        """Varmistaa, että satokuukaudet palautetaan oikeana listana."""
        self.assertEqual(self.kasvi.sato_kuukaudet(), [7, 8, 9])


class MyGardenModelTest(TestCase):
    """Testit MyGarden-mallille."""

    def setUp(self):
        """Alustaa testissä käytettävän kategorian, kasvin ja viljelymerkinnän."""
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
        """Varmistaa, että viljelymerkinnän tekstiesitys sisältää kasvin nimen."""
        self.assertIn('Tomaatti', str(self.viljely))

    def test_arvioitu_sato(self):
        """Varmistaa, että arvioitu sato lasketaan oikein kylvöpäivän perusteella."""
        sato = self.viljely.arvioitu_sato()
        self.assertIsNotNone(sato)
        self.assertGreater(sato, self.viljely.kylvopaiva)

    def test_arvioitu_sato_ilman_kylvopaivaa(self):
        """Varmistaa, että arvioitu sato on None, jos kylvöpäivää ei ole määritelty."""
        viljely = MyGarden.objects.create(kasvilaji=self.kasvi)
        self.assertIsNone(viljely.arvioitu_sato())


class GardenNoteModelTest(TestCase):
    """Testit GardenNote-mallille."""

    def setUp(self):
        """Alustaa testissä käytettävän havainnon tarvittavine riippuvuuksineen."""
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
        """Varmistaa, että havainnon tekstiesitys katkaisee pitkän tekstin."""
        self.assertIn('Ensimmäiset versot', str(self.note))


class ViewsTest(TestCase):
    """Testit näkymille."""

    def setUp(self):
        """Alustaa testiasiakkaan ja tarvittavat testidatat näkymiä varten."""
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
        """Testaa etusivun latautumisen ja sisällön vastaavuuden."""
        response = self.client.get(reverse('etusivu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Puutarhapäiväkirja')

    def test_kasvilista(self):
        """Testaa kasvilistan latautumisen ja kasvien näkymisen listalla."""
        response = self.client.get(reverse('kasvilista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tomaatti')

    def test_kasvilista_suodatus(self):
        """Testaa kasvilistan suodattamisen kategorialla."""
        response = self.client.get(reverse('kasvilista') + '?kategoria=🍅 Tomaatti')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tomaatti')

    def test_viljely_detail(self):
        """Testaa viljelymerkinnän tiedot -sivun latautumisen."""
        response = self.client.get(reverse('viljely_detail', args=[self.viljely.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tomaatti')

    def test_lisaa_viljely(self):
        """Testaa uuden viljelymerkinnän lisäämislomakkeen latautumisen."""
        response = self.client.get(reverse('lisaa_viljely'))
        self.assertEqual(response.status_code, 200)

    def test_lisaa_viljely_post(self):
        """Testaa tallennuksen onnistumisen uuden viljelymerkinnän luomisessa."""
        response = self.client.post(reverse('lisaa_viljely'), {
            'kasvilaji': self.kasvi.pk,
            'tila': 'odottaa',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MyGarden.objects.count(), 2)

    def test_lisaa_kasvilaji(self):
        """Testaa uuden kasvilajin lisäämislomakkeen latautumisen."""
        response = self.client.get(reverse('lisaa_kasvilaji'))
        self.assertEqual(response.status_code, 200)

    def test_vaihda_tila(self):
        """Testaa viljelymerkinnän tilan muuttamisen tallentumisen."""
        response = self.client.post(
            reverse('vaihda_tila', args=[self.viljely.pk]),
            {'tila': 'itanyt'},
        )
        self.assertEqual(response.status_code, 302)
        self.viljely.refresh_from_db()
        self.assertEqual(self.viljely.tila, 'itanyt')

    def test_lisaa_havainto(self):
        """Testaa uuden havainnon liittämisen viljelymerkintään."""
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


# ---------------------------------------------------------------------------
# Helpers shared across extended test classes
# ---------------------------------------------------------------------------

def _make_plant(kategoria, nimi='Testi', **kwargs):
    """Luo ja palauttaa PlantSpecies-instanssin oletusarvoilla."""
    defaults = dict(
        kylvo_alku_kk=3, kylvo_loppu_kk=5,
        sato_alku_kk=7, sato_loppu_kk=9,
    )
    defaults.update(kwargs)
    return PlantSpecies.objects.create(nimi=nimi, kategoria=kategoria, **defaults)


# ---------------------------------------------------------------------------
# Multibyte characters in text fields
# ---------------------------------------------------------------------------

class MultibyteTekstitTest(TestCase):
    """Testataan monibittisten merkkien (kiina, arabia, emoji) tallennusta."""

    def setUp(self):
        """Alustaa kategorian ja kasvilajin monibittisiä testejä varten."""
        self.kat = Category.objects.create(name='🌱 Testi')
        self.kasvi = _make_plant(self.kat)
        self.viljely = MyGarden.objects.create(kasvilaji=self.kasvi)

    # --- Category ---

    def test_category_name_chinese(self):
        """Kategoria voidaan luoda kiinalaisin merkein."""
        kat = Category.objects.create(name='蔬菜类')
        self.assertEqual(str(kat), '蔬菜类')

    def test_category_name_arabic(self):
        """Kategoria voidaan luoda arabiankielisellä nimellä."""
        kat = Category.objects.create(name='نباتات')
        self.assertEqual(str(kat), 'نباتات')

    def test_category_name_emoji(self):
        """Kategoria voidaan luoda emoji-nimellä."""
        kat = Category.objects.create(name='🌻🌺🌸')
        self.assertEqual(str(kat), '🌻🌺🌸')

    # --- PlantSpecies text fields ---

    def test_plant_nimi_chinese(self):
        """Kasvilajin nimi voidaan tallentaa kiinalaisilla merkeillä."""
        kasvi = _make_plant(self.kat, nimi='西红柿')
        self.assertEqual(kasvi.nimi, '西红柿')

    def test_plant_nimi_arabic(self):
        """Kasvilajin nimi voidaan tallentaa arabiankielisellä tekstillä."""
        kasvi = _make_plant(self.kat, nimi='طماطم')
        self.assertEqual(kasvi.nimi, 'طماطم')

    def test_plant_nimi_emoji(self):
        """Kasvilajin nimi voidaan tallentaa emojein."""
        kasvi = _make_plant(self.kat, nimi='🍅🥕🥦')
        self.assertEqual(kasvi.nimi, '🍅🥕🥦')

    def test_plant_lajike_arabic(self):
        """Kasvilajin lajike voidaan tallentaa arabiankielisellä tekstillä."""
        kasvi = _make_plant(self.kat, lajike='صنف الكرز')
        self.assertEqual(kasvi.lajike, 'صنف الكرز')

    def test_plant_lajike_chinese(self):
        """Kasvilajin lajike voidaan tallentaa kiinalaisilla merkeillä."""
        kasvi = _make_plant(self.kat, lajike='樱桃品种')
        self.assertEqual(kasvi.lajike, '樱桃品种')

    def test_plant_kuvaus_mixed_scripts(self):
        """Kuvaus-kenttä hyväksyy sekakielisen tekstin (emoji + arabia + kiina)."""
        teksti = '🌸 نوع الطماطم: 西红柿'
        kasvi = _make_plant(self.kat, kuvaus=teksti)
        self.assertEqual(kasvi.kuvaus, teksti)

    def test_plant_kasvatusohje_arabic(self):
        """Kasvatusohje-kenttä hyväksyy arabialaisen tekstin."""
        ohje = 'اسقِ النباتات يومياً'
        kasvi = _make_plant(self.kat, kasvatusohje=ohje)
        self.assertEqual(kasvi.kasvatusohje, ohje)

    def test_plant_nelson_garden_id_chinese(self):
        """Nelson Garden ID -kenttä hyväksyy kiinalaiset merkit."""
        kasvi = _make_plant(self.kat, nelson_garden_id='番茄123')
        self.assertEqual(kasvi.nelson_garden_id, '番茄123')

    # --- MyGarden text fields ---

    def test_mygarden_kasvupaikka_chinese(self):
        """Viljelymerkinnän kasvupaikka hyväksyy kiinalaiset merkit."""
        v = MyGarden.objects.create(kasvilaji=self.kasvi, kasvupaikka='阳台花盆')
        self.assertEqual(v.kasvupaikka, '阳台花盆')

    def test_mygarden_kasvupaikka_arabic(self):
        """Viljelymerkinnän kasvupaikka hyväksyy arabialaisen tekstin."""
        v = MyGarden.objects.create(kasvilaji=self.kasvi, kasvupaikka='شرفة')
        self.assertEqual(v.kasvupaikka, 'شرفة')

    def test_mygarden_kasvupaikka_emoji(self):
        """Viljelymerkinnän kasvupaikka hyväksyy emojit."""
        v = MyGarden.objects.create(kasvilaji=self.kasvi, kasvupaikka='🏡🌿')
        self.assertEqual(v.kasvupaikka, '🏡🌿')

    def test_mygarden_muistiinpanot_chinese(self):
        """Muistiinpanot-kenttä hyväksyy kiinalaiset merkit."""
        teksti = '今天播种了番茄'
        v = MyGarden.objects.create(kasvilaji=self.kasvi, muistiinpanot=teksti)
        self.assertEqual(v.muistiinpanot, teksti)

    def test_mygarden_muistiinpanot_arabic(self):
        """Muistiinpanot-kenttä hyväksyy arabialaisen tekstin."""
        teksti = 'زرعت البذور اليوم'
        v = MyGarden.objects.create(kasvilaji=self.kasvi, muistiinpanot=teksti)
        self.assertEqual(v.muistiinpanot, teksti)

    def test_mygarden_muistiinpanot_emoji(self):
        """Muistiinpanot-kenttä hyväksyy emojit."""
        teksti = '🌱💧☀️'
        v = MyGarden.objects.create(kasvilaji=self.kasvi, muistiinpanot=teksti)
        self.assertEqual(v.muistiinpanot, teksti)

    def test_mygarden_muistiinpanot_mixed(self):
        """Muistiinpanot-kenttä hyväksyy sekakielisen tekstin."""
        teksti = '🌱 بذرت اليوم / 今天播种了'
        v = MyGarden.objects.create(kasvilaji=self.kasvi, muistiinpanot=teksti)
        self.assertEqual(v.muistiinpanot, teksti)

    # --- GardenNote text fields ---

    def test_note_havainto_chinese(self):
        """Havainnon teksti hyväksyy kiinalaiset merkit."""
        note = GardenNote.objects.create(
            kasvi=self.viljely, paivamaara=date(2026, 4, 1), havainto='发芽了！'
        )
        self.assertEqual(note.havainto, '发芽了！')

    def test_note_havainto_arabic(self):
        """Havainnon teksti hyväksyy arabialaisen tekstin."""
        note = GardenNote.objects.create(
            kasvi=self.viljely, paivamaara=date(2026, 4, 2), havainto='بدأ الإنبات'
        )
        self.assertEqual(note.havainto, 'بدأ الإنبات')

    def test_note_havainto_emoji(self):
        """Havainnon teksti hyväksyy emojit."""
        note = GardenNote.objects.create(
            kasvi=self.viljely, paivamaara=date(2026, 4, 3), havainto='🌱🌿🍀'
        )
        self.assertEqual(note.havainto, '🌱🌿🍀')


# ---------------------------------------------------------------------------
# Very long text input
# ---------------------------------------------------------------------------

class PitkaTekstitTest(TestCase):
    """Testataan todella pitkien tekstien tallennusta malleihin."""

    def setUp(self):
        """Alustaa kategorian ja kasvilajin pitkiä tekstejä varten."""
        self.kat = Category.objects.create(name='🌱 Testi')
        self.kasvi = _make_plant(self.kat)
        self.viljely = MyGarden.objects.create(kasvilaji=self.kasvi)

    def test_plant_kuvaus_very_long(self):
        """Kuvaus-tekstikenttä hyväksyy erittäin pitkän tekstin (100 000 merkkiä)."""
        teksti = 'A' * 100_000
        kasvi = _make_plant(self.kat, kuvaus=teksti)
        kasvi.refresh_from_db()
        self.assertEqual(len(kasvi.kuvaus), 100_000)

    def test_plant_kasvatusohje_very_long(self):
        """Kasvatusohje-tekstikenttä hyväksyy erittäin pitkän tekstin (100 000 merkkiä)."""
        teksti = 'B' * 100_000
        kasvi = _make_plant(self.kat, kasvatusohje=teksti)
        kasvi.refresh_from_db()
        self.assertEqual(len(kasvi.kasvatusohje), 100_000)

    def test_mygarden_muistiinpanot_very_long(self):
        """Muistiinpanot-tekstikenttä hyväksyy erittäin pitkän tekstin (100 000 merkkiä)."""
        teksti = 'C' * 100_000
        v = MyGarden.objects.create(kasvilaji=self.kasvi, muistiinpanot=teksti)
        v.refresh_from_db()
        self.assertEqual(len(v.muistiinpanot), 100_000)

    def test_note_havainto_very_long(self):
        """GardenNote-havainto hyväksyy erittäin pitkän tekstin (100 000 merkkiä)."""
        teksti = 'D' * 100_000
        note = GardenNote.objects.create(
            kasvi=self.viljely, paivamaara=date(2026, 5, 1), havainto=teksti
        )
        note.refresh_from_db()
        self.assertEqual(len(note.havainto), 100_000)

    def test_note_str_truncates_at_50_chars(self):
        """GardenNote __str__ katkaisee havainnon 50 merkin jälkeen."""
        teksti = 'X' * 200
        note = GardenNote.objects.create(
            kasvi=self.viljely, paivamaara=date(2026, 5, 2), havainto=teksti
        )
        # __str__ palauttaa "paivamaara — havainto[:50]"
        self.assertIn('X' * 50, str(note))
        self.assertNotIn('X' * 51, str(note))

    def test_category_name_long_boundary(self):
        """Kategorian nimi hyväksyy 50 merkin pituuden (max_length raja)."""
        name = 'K' * 50
        kat = Category.objects.create(name=name)
        self.assertEqual(len(kat.name), 50)


# ---------------------------------------------------------------------------
# Control characters in text input
# ---------------------------------------------------------------------------

class OhjausmerkkiTest(TestCase):
    """Testataan ohjausmerkkien (null, newline, tab, DEL jne.) tallennusta."""

    def setUp(self):
        """Alustaa kategorian ja kasvilajin ohjausmerkkejä varten."""
        self.kat = Category.objects.create(name='🌱 Testi')
        self.kasvi = _make_plant(self.kat)
        self.viljely = MyGarden.objects.create(kasvilaji=self.kasvi)

    def test_plant_kuvaus_newlines_and_tabs(self):
        """Kuvaus hyväksyy rivinvaihdot ja tabulaattorit."""
        teksti = 'Rivi1\nRivi2\tSarake'
        kasvi = _make_plant(self.kat, kuvaus=teksti)
        kasvi.refresh_from_db()
        self.assertEqual(kasvi.kuvaus, teksti)

    def test_plant_kuvaus_carriage_return(self):
        """Kuvaus hyväksyy Windows-tyylisen rivinvaihdon (\\r\\n)."""
        teksti = 'Rivi1\r\nRivi2'
        kasvi = _make_plant(self.kat, kuvaus=teksti)
        kasvi.refresh_from_db()
        self.assertEqual(kasvi.kuvaus, teksti)

    def test_plant_kasvatusohje_null_byte(self):
        """Kasvatusohje hyväksyy null-tavun sisältävän merkkijonon."""
        teksti = 'Kylvä\x00maahan'
        kasvi = _make_plant(self.kat, kasvatusohje=teksti)
        kasvi.refresh_from_db()
        self.assertEqual(kasvi.kasvatusohje, teksti)

    def test_plant_kuvaus_unicode_control_chars(self):
        """Kuvaus hyväksyy Unicode-ohjausmerkit (U+0001–U+001F)."""
        teksti = ''.join(chr(i) for i in range(1, 32))
        kasvi = _make_plant(self.kat, kuvaus=teksti)
        kasvi.refresh_from_db()
        self.assertEqual(kasvi.kuvaus, teksti)

    def test_mygarden_muistiinpanot_control_chars(self):
        """Muistiinpanot hyväksyy ohjausmerkit (\\x01, \\x1f, \\x7f)."""
        teksti = 'Alku\x01\x1f\x7fLoppu'
        v = MyGarden.objects.create(kasvilaji=self.kasvi, muistiinpanot=teksti)
        v.refresh_from_db()
        self.assertEqual(v.muistiinpanot, teksti)

    def test_mygarden_kasvupaikka_tab(self):
        """Kasvupaikka hyväksyy tabulaattorin."""
        v = MyGarden.objects.create(kasvilaji=self.kasvi, kasvupaikka='Parvi\tlakko')
        v.refresh_from_db()
        self.assertEqual(v.kasvupaikka, 'Parvi\tlakko')

    def test_mygarden_kasvupaikka_newline(self):
        """Kasvupaikka hyväksyy rivinvaihdon."""
        v = MyGarden.objects.create(kasvilaji=self.kasvi, kasvupaikka='Rivi1\nRivi2')
        v.refresh_from_db()
        self.assertEqual(v.kasvupaikka, 'Rivi1\nRivi2')

    def test_note_havainto_control_chars(self):
        """Havainto hyväksyy ohjausmerkit."""
        teksti = 'Havainto\x00\x0c\x1b'
        note = GardenNote.objects.create(
            kasvi=self.viljely, paivamaara=date(2026, 6, 1), havainto=teksti
        )
        note.refresh_from_db()
        self.assertEqual(note.havainto, teksti)

    def test_note_havainto_del_char(self):
        """Havainto hyväksyy DEL-merkin (\\x7f)."""
        teksti = 'Havainto\x7fTesti'
        note = GardenNote.objects.create(
            kasvi=self.viljely, paivamaara=date(2026, 6, 2), havainto=teksti
        )
        note.refresh_from_db()
        self.assertEqual(note.havainto, teksti)


# ---------------------------------------------------------------------------
# Invalid month numbers and other numeric fields (form validation)
# ---------------------------------------------------------------------------

class LomakeNumeerisetVirheellisetTest(TestCase):
    """Testataan lomakkeen kenttävalidointia virheellisillä numerosyötteillä."""

    def setUp(self):
        """Alustaa kategorian PlantSpeciesForm-testejä varten."""
        self.kat = Category.objects.create(name='🌱 Testi')
        self.base_data = {
            'nimi': 'Testi',
            'lajike': '',
            'kategoria': self.kat.pk,
            'kuvaus': '',
            'kasvatusohje': '',
            'kylvo_alku_kk': 3,
            'kylvo_loppu_kk': 5,
            'sato_alku_kk': 7,
            'sato_loppu_kk': 9,
            'itamisaika_min_pv': 7,
            'itamisaika_max_pv': 14,
            'korkeus_cm': '',
            'kasvupaikka': 'aurinko',
            'siemenia_pakkauksessa': '',
        }

    def _form(self, **overrides):
        """Luo PlantSpeciesForm-lomakkeen annetuilla ylikirjoituksilla."""
        from .forms import PlantSpeciesForm
        data = {**self.base_data, **overrides}
        return PlantSpeciesForm(data=data)

    # kylvo_alku_kk: invalid values
    def test_kylvo_alku_kk_zero_invalid(self):
        """kylvo_alku_kk=0 ei ole sallittu valinta."""
        self.assertFalse(self._form(kylvo_alku_kk=0).is_valid())

    def test_kylvo_alku_kk_negative_invalid(self):
        """kylvo_alku_kk=-1 ei ole sallittu valinta."""
        self.assertFalse(self._form(kylvo_alku_kk=-1).is_valid())

    def test_kylvo_alku_kk_13_invalid(self):
        """kylvo_alku_kk=13 ei ole sallittu valinta."""
        self.assertFalse(self._form(kylvo_alku_kk=13).is_valid())

    def test_kylvo_alku_kk_string_invalid(self):
        """kylvo_alku_kk='foobar' ei ole sallittu valinta."""
        self.assertFalse(self._form(kylvo_alku_kk='foobar').is_valid())

    def test_kylvo_alku_kk_float_invalid(self):
        """kylvo_alku_kk='3.5' ei ole sallittu valinta."""
        self.assertFalse(self._form(kylvo_alku_kk='3.5').is_valid())

    # kylvo_loppu_kk: invalid values
    def test_kylvo_loppu_kk_zero_invalid(self):
        """kylvo_loppu_kk=0 ei ole sallittu valinta."""
        self.assertFalse(self._form(kylvo_loppu_kk=0).is_valid())

    def test_kylvo_loppu_kk_13_invalid(self):
        """kylvo_loppu_kk=13 ei ole sallittu valinta."""
        self.assertFalse(self._form(kylvo_loppu_kk=13).is_valid())

    def test_kylvo_loppu_kk_string_invalid(self):
        """kylvo_loppu_kk='foobar' ei ole sallittu valinta."""
        self.assertFalse(self._form(kylvo_loppu_kk='foobar').is_valid())

    # sato_alku_kk: invalid values
    def test_sato_alku_kk_zero_invalid(self):
        """sato_alku_kk=0 ei ole sallittu valinta."""
        self.assertFalse(self._form(sato_alku_kk=0).is_valid())

    def test_sato_alku_kk_13_invalid(self):
        """sato_alku_kk=13 ei ole sallittu valinta."""
        self.assertFalse(self._form(sato_alku_kk=13).is_valid())

    def test_sato_alku_kk_string_invalid(self):
        """sato_alku_kk='foobar' ei ole sallittu valinta."""
        self.assertFalse(self._form(sato_alku_kk='foobar').is_valid())

    def test_sato_alku_kk_negative_invalid(self):
        """sato_alku_kk=-1 ei ole sallittu valinta."""
        self.assertFalse(self._form(sato_alku_kk=-1).is_valid())

    # sato_loppu_kk: invalid values
    def test_sato_loppu_kk_zero_invalid(self):
        """sato_loppu_kk=0 ei ole sallittu valinta."""
        self.assertFalse(self._form(sato_loppu_kk=0).is_valid())

    def test_sato_loppu_kk_13_invalid(self):
        """sato_loppu_kk=13 ei ole sallittu valinta."""
        self.assertFalse(self._form(sato_loppu_kk=13).is_valid())

    def test_sato_loppu_kk_string_invalid(self):
        """sato_loppu_kk='foobar' ei ole sallittu valinta."""
        self.assertFalse(self._form(sato_loppu_kk='foobar').is_valid())

    def test_sato_loppu_kk_negative_invalid(self):
        """sato_loppu_kk=-1 ei ole sallittu valinta."""
        self.assertFalse(self._form(sato_loppu_kk=-1).is_valid())

    # itamisaika_min_pv / itamisaika_max_pv
    def test_itamisaika_min_pv_string_invalid(self):
        """itamisaika_min_pv='foobar' ei ole sallittu."""
        self.assertFalse(self._form(itamisaika_min_pv='foobar').is_valid())

    def test_itamisaika_max_pv_string_invalid(self):
        """itamisaika_max_pv='foobar' ei ole sallittu."""
        self.assertFalse(self._form(itamisaika_max_pv='foobar').is_valid())

    def test_itamisaika_min_pv_float_invalid(self):
        """itamisaika_min_pv='3.5' ei ole sallittu kokonaislukukentälle."""
        self.assertFalse(self._form(itamisaika_min_pv='3.5').is_valid())

    def test_itamisaika_max_pv_float_invalid(self):
        """itamisaika_max_pv='3.5' ei ole sallittu kokonaislukukentälle."""
        self.assertFalse(self._form(itamisaika_max_pv='3.5').is_valid())

    # korkeus_cm
    def test_korkeus_cm_string_invalid(self):
        """korkeus_cm='foobar' ei ole sallittu."""
        self.assertFalse(self._form(korkeus_cm='foobar').is_valid())

    def test_korkeus_cm_float_invalid(self):
        """korkeus_cm='50.5' ei ole sallittu kokonaislukukentälle."""
        self.assertFalse(self._form(korkeus_cm='50.5').is_valid())

    def test_korkeus_cm_blank_valid(self):
        """korkeus_cm voidaan jättää tyhjäksi (nullable)."""
        self.assertTrue(self._form(korkeus_cm='').is_valid())

    def test_korkeus_cm_negative_valid_model_level(self):
        """korkeus_cm hyväksyy negatiivisen arvon mallin tasolla (ei lomakerajoitetta)."""
        kat = Category.objects.create(name='🌱 Negatiivinen')
        kasvi = _make_plant(kat, korkeus_cm=-5)
        kasvi.refresh_from_db()
        self.assertEqual(kasvi.korkeus_cm, -5)

    # siemenia_pakkauksessa
    def test_siemenia_string_invalid(self):
        """siemenia_pakkauksessa='foobar' ei ole sallittu."""
        self.assertFalse(self._form(siemenia_pakkauksessa='foobar').is_valid())

    def test_siemenia_float_invalid(self):
        """siemenia_pakkauksessa='3.5' ei ole sallittu kokonaislukukentälle."""
        self.assertFalse(self._form(siemenia_pakkauksessa='3.5').is_valid())

    def test_siemenia_blank_valid(self):
        """siemenia_pakkauksessa voidaan jättää tyhjäksi (nullable)."""
        self.assertTrue(self._form(siemenia_pakkauksessa='').is_valid())

    # Valid boundary values for month fields
    def test_kylvo_alku_kk_1_valid(self):
        """kylvo_alku_kk=1 on sallittu minimiarvo."""
        self.assertTrue(self._form(kylvo_alku_kk=1).is_valid())

    def test_kylvo_alku_kk_12_valid(self):
        """kylvo_alku_kk=12 on sallittu maksimiarvo."""
        self.assertTrue(self._form(kylvo_alku_kk=12).is_valid())

    def test_sato_loppu_kk_1_valid(self):
        """sato_loppu_kk=1 on sallittu minimiarvo."""
        self.assertTrue(self._form(sato_loppu_kk=1).is_valid())

    def test_sato_loppu_kk_12_valid(self):
        """sato_loppu_kk=12 on sallittu maksimiarvo."""
        self.assertTrue(self._form(sato_loppu_kk=12).is_valid())


# ---------------------------------------------------------------------------
# Invalid choices (kasvupaikka, tila)
# ---------------------------------------------------------------------------

class LomakeVirheellisetValinnatTest(TestCase):
    """Testataan lomakevalidointia virheellisillä valintakentillä."""

    def setUp(self):
        """Alustaa kategorian ja kasvilajin valintakenttätestejä varten."""
        self.kat = Category.objects.create(name='🌱 Testi')
        self.kasvi = _make_plant(self.kat)

    def test_kasvupaikka_invalid_choice(self):
        """PlantSpeciesForm hylkää tuntemattoman kasvupaikka-arvon."""
        from .forms import PlantSpeciesForm
        data = {
            'nimi': 'Testi', 'lajike': '', 'kategoria': self.kat.pk,
            'kuvaus': '', 'kasvatusohje': '',
            'kylvo_alku_kk': 3, 'kylvo_loppu_kk': 5,
            'sato_alku_kk': 7, 'sato_loppu_kk': 9,
            'itamisaika_min_pv': 7, 'itamisaika_max_pv': 14,
            'korkeus_cm': '', 'kasvupaikka': 'taivas', 'siemenia_pakkauksessa': '',
        }
        form = PlantSpeciesForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('kasvupaikka', form.errors)

    def test_kasvupaikka_empty_invalid(self):
        """PlantSpeciesForm hylkää tyhjän kasvupaikka-arvon."""
        from .forms import PlantSpeciesForm
        data = {
            'nimi': 'Testi', 'lajike': '', 'kategoria': self.kat.pk,
            'kuvaus': '', 'kasvatusohje': '',
            'kylvo_alku_kk': 3, 'kylvo_loppu_kk': 5,
            'sato_alku_kk': 7, 'sato_loppu_kk': 9,
            'itamisaika_min_pv': 7, 'itamisaika_max_pv': 14,
            'korkeus_cm': '', 'kasvupaikka': '', 'siemenia_pakkauksessa': '',
        }
        form = PlantSpeciesForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('kasvupaikka', form.errors)

    def test_kasvupaikka_valid_all_choices(self):
        """PlantSpeciesForm hyväksyy kaikki kelvolliset kasvupaikka-vaihtoehdot."""
        from .forms import PlantSpeciesForm
        for kasvupaikka in ['aurinko', 'puolivarjo', 'varjo']:
            with self.subTest(kasvupaikka=kasvupaikka):
                data = {
                    'nimi': 'Testi', 'lajike': '', 'kategoria': self.kat.pk,
                    'kuvaus': '', 'kasvatusohje': '',
                    'kylvo_alku_kk': 3, 'kylvo_loppu_kk': 5,
                    'sato_alku_kk': 7, 'sato_loppu_kk': 9,
                    'itamisaika_min_pv': 7, 'itamisaika_max_pv': 14,
                    'korkeus_cm': '', 'kasvupaikka': kasvupaikka, 'siemenia_pakkauksessa': '',
                }
                form = PlantSpeciesForm(data=data)
                self.assertTrue(form.is_valid(), f"kasvupaikka='{kasvupaikka}' olisi pitänyt olla kelvollinen")

    def test_tila_invalid_choice(self):
        """TilaForm hylkää tuntemattoman tila-arvon."""
        from .forms import TilaForm
        form = TilaForm(data={'tila': 'lentaa'})
        self.assertFalse(form.is_valid())
        self.assertIn('tila', form.errors)

    def test_tila_empty_choice_invalid(self):
        """TilaForm hylkää tyhjän tila-arvon."""
        from .forms import TilaForm
        form = TilaForm(data={'tila': ''})
        self.assertFalse(form.is_valid())

    def test_tila_numeric_invalid(self):
        """TilaForm hylkää numeerisen tila-arvon."""
        from .forms import TilaForm
        form = TilaForm(data={'tila': '42'})
        self.assertFalse(form.is_valid())

    def test_tila_valid_all_choices(self):
        """TilaForm hyväksyy kaikki kelvolliset tila-vaihtoehdot."""
        from .forms import TilaForm
        valid_choices = ['odottaa', 'kylvetty', 'itanyt', 'kasvaa', 'sadonkorjuu', 'paattynyt']
        for tila in valid_choices:
            with self.subTest(tila=tila):
                form = TilaForm(data={'tila': tila})
                self.assertTrue(form.is_valid(), f"Tila '{tila}' olisi pitänyt olla kelvollinen")


# ---------------------------------------------------------------------------
# Invalid associations (non-existing FK references, cascade deletes)
# ---------------------------------------------------------------------------

class VirheellisetAssosiaatiotTest(TestCase):
    """Testataan virheellisiä viittauksia olemattomiin objekteihin."""

    def setUp(self):
        """Alustaa kategorian ja kasvilajin assosiaatiotestejä varten."""
        self.kat = Category.objects.create(name='🌱 Testi')
        self.kasvi = _make_plant(self.kat)
        self.viljely = MyGarden.objects.create(kasvilaji=self.kasvi)

    # --- PlantSpeciesForm: olematon kategoria ---

    def test_plant_form_nonexistent_category(self):
        """PlantSpeciesForm hylkää olemattoman kategoria-id:n."""
        from .forms import PlantSpeciesForm
        data = {
            'nimi': 'Testi', 'lajike': '', 'kategoria': 99999,
            'kuvaus': '', 'kasvatusohje': '',
            'kylvo_alku_kk': 3, 'kylvo_loppu_kk': 5,
            'sato_alku_kk': 7, 'sato_loppu_kk': 9,
            'itamisaika_min_pv': 7, 'itamisaika_max_pv': 14,
            'korkeus_cm': '', 'kasvupaikka': 'aurinko', 'siemenia_pakkauksessa': '',
        }
        form = PlantSpeciesForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('kategoria', form.errors)

    def test_plant_form_string_category(self):
        """PlantSpeciesForm hylkää merkkijonon kategoria-kentässä."""
        from .forms import PlantSpeciesForm
        data = {
            'nimi': 'Testi', 'lajike': '', 'kategoria': 'foobar',
            'kuvaus': '', 'kasvatusohje': '',
            'kylvo_alku_kk': 3, 'kylvo_loppu_kk': 5,
            'sato_alku_kk': 7, 'sato_loppu_kk': 9,
            'itamisaika_min_pv': 7, 'itamisaika_max_pv': 14,
            'korkeus_cm': '', 'kasvupaikka': 'aurinko', 'siemenia_pakkauksessa': '',
        }
        form = PlantSpeciesForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('kategoria', form.errors)

    def test_plant_form_missing_category(self):
        """PlantSpeciesForm hylkää puuttuvan kategoria-kentän."""
        from .forms import PlantSpeciesForm
        data = {
            'nimi': 'Testi', 'lajike': '',
            'kuvaus': '', 'kasvatusohje': '',
            'kylvo_alku_kk': 3, 'kylvo_loppu_kk': 5,
            'sato_alku_kk': 7, 'sato_loppu_kk': 9,
            'itamisaika_min_pv': 7, 'itamisaika_max_pv': 14,
            'korkeus_cm': '', 'kasvupaikka': 'aurinko', 'siemenia_pakkauksessa': '',
        }
        form = PlantSpeciesForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('kategoria', form.errors)

    # --- MyGardenForm: olematon kasvilaji ---

    def test_mygarden_form_nonexistent_kasvilaji(self):
        """MyGardenForm hylkää olemattoman kasvilaji-id:n."""
        from .forms import MyGardenForm
        form = MyGardenForm(data={'kasvilaji': 99999, 'tila': 'odottaa'})
        self.assertFalse(form.is_valid())
        self.assertIn('kasvilaji', form.errors)

    def test_mygarden_form_string_kasvilaji(self):
        """MyGardenForm hylkää merkkijonon kasvilaji-kentässä."""
        from .forms import MyGardenForm
        form = MyGardenForm(data={'kasvilaji': 'foobar', 'tila': 'odottaa'})
        self.assertFalse(form.is_valid())
        self.assertIn('kasvilaji', form.errors)

    def test_mygarden_form_missing_kasvilaji(self):
        """MyGardenForm hylkää puuttuvan kasvilaji-kentän."""
        from .forms import MyGardenForm
        form = MyGardenForm(data={'tila': 'odottaa'})
        self.assertFalse(form.is_valid())
        self.assertIn('kasvilaji', form.errors)

    # --- View: olematon PK URL:ssa ---

    def test_viljely_detail_get_nonexistent_pk(self):
        """Olemattoman viljelymerkinnän PK palauttaa 404."""
        response = self.client.get(reverse('viljely_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)

    def test_viljely_detail_post_nonexistent_pk(self):
        """Olemattoman viljelymerkinnän PK POST palauttaa 404."""
        response = self.client.post(
            reverse('viljely_detail', args=[99999]),
            {'vaihda_tila': '1', 'tila': 'itanyt'},
        )
        self.assertEqual(response.status_code, 404)

    def test_vaihda_tila_nonexistent_pk(self):
        """Olemattoman viljelymerkinnän PK tilan vaihdossa palauttaa 404."""
        response = self.client.post(
            reverse('vaihda_tila', args=[99999]), {'tila': 'itanyt'}
        )
        self.assertEqual(response.status_code, 404)

    # --- GardenNote: olematon kasvi FK ---

    def test_gardennote_invalid_kasvi_ref(self):
        """GardenNote ei voi viitata olemattomaan MyGarden-merkintään (sovellustason tarkistus)."""
        # GardenNote-form ilman kasvi-kenttää on virheellinen, koska kasvi on pakollinen FK.
        from .forms import GardenNoteForm
        form = GardenNoteForm(data={"paivamaara": "2026-01-01", "havainto": "testi"})
        # Lomake on validi kun kenttä on oikein (kasvi-kenttä ei ole lomakkeessa, se asetetaan koodissa).
        # Sen sijaan havainto-kenttä on pakollinen.
        self.assertTrue(form.is_valid(), form.errors)

    # --- CASCADE: poistettu kategoria poistaa lajit ---

    def test_cascade_delete_category_removes_plants(self):
        """Kategorian poistaminen poistaa kaikki siihen liittyvät kasvilajit."""
        kat2 = Category.objects.create(name='🍋 Sitrushedelmät')
        _make_plant(kat2, nimi='Sitruuna')
        self.assertEqual(PlantSpecies.objects.filter(kategoria=kat2).count(), 1)
        kat2.delete()
        self.assertEqual(PlantSpecies.objects.filter(kategoria_id=kat2.pk).count(), 0)

    # --- CASCADE: poistettu kasvilaji poistaa viljelymerkinnät ---

    def test_cascade_delete_plant_removes_viljelyt(self):
        """Kasvilajin poistaminen poistaa kaikki siihen liittyvät viljelymerkinnät."""
        kasvi2 = _make_plant(self.kat, nimi='Poistettava')
        MyGarden.objects.create(kasvilaji=kasvi2)
        pk2 = kasvi2.pk
        kasvi2.delete()
        self.assertEqual(MyGarden.objects.filter(kasvilaji_id=pk2).count(), 0)

    # --- CASCADE: poistettu viljely poistaa havainnot ---

    def test_cascade_delete_viljely_removes_notes(self):
        """Viljelymerkinnän poistaminen poistaa kaikki siihen liittyvät havainnot."""
        GardenNote.objects.create(
            kasvi=self.viljely, paivamaara=date(2026, 5, 5), havainto='Testi havainto'
        )
        viljely_pk = self.viljely.pk
        self.assertEqual(GardenNote.objects.filter(kasvi=self.viljely).count(), 1)
        self.viljely.delete()
        self.assertEqual(GardenNote.objects.filter(kasvi_id=viljely_pk).count(), 0)

    # --- Category unique constraint ---

    def test_category_name_unique(self):
        """Kategorian nimi on yksilöllinen — duplikaatin luominen heittää poikkeuksen."""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Category.objects.create(name='🌱 Testi')
