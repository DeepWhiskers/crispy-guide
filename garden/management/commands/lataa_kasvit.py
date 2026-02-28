"""Lataa esimerkkikasvit tietokantaan."""
from django.core.management.base import BaseCommand
from garden.models import PlantSpecies, Category


KASVIT = [
    {
        'nelson_garden_id': '91706',
        'nimi': 'Kirsikkatomaatti',
        'lajike': 'Sungold F1',
        'kategoria': 'Tomaatti',
        'kuvaus': 'Testien mukaan maailman makein kirsikkatomaatti. Tuottaa runsaasti pieniä, oransseja ja meheviä hedelmiä.',
        'kasvatusohje': 'Esikasvatus sisätiloissa ruukuissa helmikuusta alkaen. Istuta ulos kasvihuoneeseen tai lämpimälle paikalle toukokuussa.',
        'kylvo_alku_kk': 2, 'kylvo_loppu_kk': 4,
        'sato_alku_kk': 7, 'sato_loppu_kk': 9,
        'itamisaika_min_pv': 5, 'itamisaika_max_pv': 15,
        'korkeus_cm': 150, 'kasvupaikka': 'aurinko',
        'siemenia_pakkauksessa': 7,
    },
    {
        'nelson_garden_id': '91503',
        'nimi': 'Tomaatti',
        'lajike': 'Black Cherry',
        'kategoria': 'Tomaatti',
        'kuvaus': 'Tummanpunainen, lähes musta kirsikkatomaatti. Runsas ja makea sato.',
        'kasvatusohje': 'Esikasvatus sisällä. Vaatii tuennan kasvaessaan.',
        'kylvo_alku_kk': 2, 'kylvo_loppu_kk': 4,
        'sato_alku_kk': 7, 'sato_loppu_kk': 9,
        'itamisaika_min_pv': 7, 'itamisaika_max_pv': 14,
        'korkeus_cm': 180, 'kasvupaikka': 'aurinko',
        'siemenia_pakkauksessa': 8,
    },
    {
        'nimi': 'Basilika',
        'lajike': 'Genovese',
        'kategoria': 'Yrtit',
        'kuvaus': 'Klassinen italialainen basilika, tuuheakasvuinen ja aromaattinen.',
        'kasvatusohje': 'Kylvä sisälle tai suoraan maahan toukokuun jälkeen. Nypitään kukkavarret pois.',
        'kylvo_alku_kk': 3, 'kylvo_loppu_kk': 5,
        'sato_alku_kk': 6, 'sato_loppu_kk': 9,
        'itamisaika_min_pv': 5, 'itamisaika_max_pv': 10,
        'korkeus_cm': 40, 'kasvupaikka': 'aurinko',
        'siemenia_pakkauksessa': 600,
    },
    {
        'nimi': 'Tilli',
        'lajike': '',
        'kategoria': 'Yrtit',
        'kuvaus': 'Suosittu suomalainen yrtti kalalle ja perunoille. Helppokasvatteinen.',
        'kasvatusohje': 'Kylvä suoraan maahan keväällä. Viihtyy aurinkoisella paikalla.',
        'kylvo_alku_kk': 4, 'kylvo_loppu_kk': 6,
        'sato_alku_kk': 6, 'sato_loppu_kk': 9,
        'itamisaika_min_pv': 10, 'itamisaika_max_pv': 18,
        'korkeus_cm': 60, 'kasvupaikka': 'aurinko',
        'siemenia_pakkauksessa': 1000,
    },
    {
        'nimi': 'Persilja',
        'lajike': 'Moss Curled',
        'kategoria': 'Yrtit',
        'kuvaus': 'Kihara persilja, monipuolinen mausteyrtti.',
        'kasvatusohje': 'Kylvä sisälle aikaisin keväällä tai suoraan maahan. Itää hitaasti.',
        'kylvo_alku_kk': 3, 'kylvo_loppu_kk': 5,
        'sato_alku_kk': 6, 'sato_loppu_kk': 10,
        'itamisaika_min_pv': 14, 'itamisaika_max_pv': 28,
        'korkeus_cm': 30, 'kasvupaikka': 'puolivarjo',
        'siemenia_pakkauksessa': 800,
    },
    {
        'nimi': 'Salaatti',
        'lajike': 'Frillice',
        'kategoria': 'Salaatti',
        'kuvaus': 'Rapea ja kestävä jäävuorityyppinen salaatti, erinomainen parvekeviljelyyn.',
        'kasvatusohje': 'Kylvä suoraan ruukkuun tai penkkiin. Viihtyy viileämmässäkin säässä.',
        'kylvo_alku_kk': 4, 'kylvo_loppu_kk': 7,
        'sato_alku_kk': 6, 'sato_loppu_kk': 9,
        'itamisaika_min_pv': 5, 'itamisaika_max_pv': 10,
        'korkeus_cm': 25, 'kasvupaikka': 'puolivarjo',
        'siemenia_pakkauksessa': 500,
    },
    {
        'nimi': 'Rucolasalaatti',
        'lajike': '',
        'kategoria': 'Salaatti',
        'kuvaus': 'Pippurinen ja maukas salaattikasvi. Nopea kasvuinen.',
        'kasvatusohje': 'Kylvä suoraan maahan tai ruukkuun. Kerää lehtiä sitä mukaa kun ne kasvavat.',
        'kylvo_alku_kk': 4, 'kylvo_loppu_kk': 8,
        'sato_alku_kk': 5, 'sato_loppu_kk': 10,
        'itamisaika_min_pv': 3, 'itamisaika_max_pv': 7,
        'korkeus_cm': 20, 'kasvupaikka': 'puolivarjo',
        'siemenia_pakkauksessa': 700,
    },
    {
        'nimi': 'Kurkku',
        'lajike': 'Marketmore',
        'kategoria': 'Vihannekset',
        'kuvaus': 'Perinteinen avomaan kurkku. Tuottaa runsaasti tummia, rapeita kurkkuja.',
        'kasvatusohje': 'Esikasvatus sisätiloissa huhtikuussa. Istuta ulos lämpimän sään alettua.',
        'kylvo_alku_kk': 4, 'kylvo_loppu_kk': 5,
        'sato_alku_kk': 7, 'sato_loppu_kk': 9,
        'itamisaika_min_pv': 5, 'itamisaika_max_pv': 10,
        'korkeus_cm': 200, 'kasvupaikka': 'aurinko',
        'siemenia_pakkauksessa': 25,
    },
    {
        'nimi': 'Kesäkurpitsa',
        'lajike': 'Black Beauty',
        'kategoria': 'Vihannekset',
        'kuvaus': 'Klassinen tummanvihreä kesäkurpitsa eli zucchini. Erittäin satoisa.',
        'kasvatusohje': 'Esikasvatus sisällä tai kylvö suoraan maahan kesäkuun alussa.',
        'kylvo_alku_kk': 4, 'kylvo_loppu_kk': 6,
        'sato_alku_kk': 7, 'sato_loppu_kk': 9,
        'itamisaika_min_pv': 5, 'itamisaika_max_pv': 10,
        'korkeus_cm': 60, 'kasvupaikka': 'aurinko',
        'siemenia_pakkauksessa': 15,
    },
    {
        'nimi': 'Porkkana',
        'lajike': 'Nantes',
        'kategoria': 'Juurekset',
        'kuvaus': 'Makea ja rapea porkkana. Sopii hyvin Suomen oloihin.',
        'kasvatusohje': 'Kylvä suoraan penkkiin keväällä. Vaatii kuohkean maan.',
        'kylvo_alku_kk': 5, 'kylvo_loppu_kk': 6,
        'sato_alku_kk': 8, 'sato_loppu_kk': 10,
        'itamisaika_min_pv': 10, 'itamisaika_max_pv': 21,
        'korkeus_cm': 30, 'kasvupaikka': 'aurinko',
        'siemenia_pakkauksessa': 2000,
    },
    {
        'nimi': 'Retiisi',
        'lajike': 'Cherry Belle',
        'kategoria': 'Juurekset',
        'kuvaus': 'Nopea ja helppo juureksi. Valmis 3-4 viikossa kylvöstä.',
        'kasvatusohje': 'Kylvä suoraan maahan tai ruukkuun. Pidä maa kosteana.',
        'kylvo_alku_kk': 4, 'kylvo_loppu_kk': 8,
        'sato_alku_kk': 5, 'sato_loppu_kk': 9,
        'itamisaika_min_pv': 3, 'itamisaika_max_pv': 7,
        'korkeus_cm': 15, 'kasvupaikka': 'aurinko',
        'siemenia_pakkauksessa': 500,
    },
    {
        'nimi': 'Chili',
        'lajike': 'Jalapeño',
        'kategoria': 'Chili',
        'kuvaus': 'Keskivahva chili, sopii tulisiin ruokiin ja säilöntään. 2500-8000 SHU.',
        'kasvatusohje': 'Aloita esikasvatus jo tammikuussa. Vaatii lämpöä ja valoa.',
        'kylvo_alku_kk': 1, 'kylvo_loppu_kk': 3,
        'sato_alku_kk': 7, 'sato_loppu_kk': 10,
        'itamisaika_min_pv': 10, 'itamisaika_max_pv': 21,
        'korkeus_cm': 70, 'kasvupaikka': 'aurinko',
        'siemenia_pakkauksessa': 20,
    },
    {
        'nimi': 'Mansikka',
        'lajike': 'Alexandria',
        'kategoria': 'Marjat',
        'kuvaus': 'Ahomansikka, pienikokoinen mutta erittäin maukas. Sopii ruukkuviljelyyn.',
        'kasvatusohje': 'Kylvä sisällä aikaisin keväällä. Siemenet tarvitsevat valoa itääkseen.',
        'kylvo_alku_kk': 2, 'kylvo_loppu_kk': 4,
        'sato_alku_kk': 7, 'sato_loppu_kk': 9,
        'itamisaika_min_pv': 14, 'itamisaika_max_pv': 30,
        'korkeus_cm': 20, 'kasvupaikka': 'aurinko',
        'siemenia_pakkauksessa': 100,
    },
    {
        'nimi': 'Herne',
        'lajike': 'Kelvedon Wonder',
        'kategoria': 'Palkokasvit',
        'kuvaus': 'Perinteinen puutarhaherne, makea ja rapea. Matalakasvuinen.',
        'kasvatusohje': 'Kylvä suoraan maahan toukokuussa. Tarvitsee tukiverkon.',
        'kylvo_alku_kk': 5, 'kylvo_loppu_kk': 6,
        'sato_alku_kk': 7, 'sato_loppu_kk': 8,
        'itamisaika_min_pv': 7, 'itamisaika_max_pv': 14,
        'korkeus_cm': 50, 'kasvupaikka': 'aurinko',
        'siemenia_pakkauksessa': 75,
    },
]


class Command(BaseCommand):
    help = 'Lataa esimerkkikasvit tietokantaan'

    def handle(self, *args, **options):
        # Mappings for initial setup
        category_map = {
            'Chili': '🌶️ Chili',
            'Juurekset': '🥕 Juurekset',
            'Marjat': '🍓 Marjat',
            'Palkokasvit': '🫛 Palkokasvit',
            'Salaatti': '🥬 Salaatti',
            'Tomaatti': '🍅 Tomaatti',
            'Vihannekset': '🥦 Vihannekset',
            'Yrtit': '🌿 Yrtit',
        }
        
        created_count = 0
        for raw_data in KASVIT:
            data = raw_data.copy()
            
            old_cat = data.pop('kategoria')
            new_name = category_map.get(old_cat, f"🌱 {old_cat}")
            category_obj, _ = Category.objects.get_or_create(name=new_name)
            
            data['kategoria'] = category_obj

            obj, created = PlantSpecies.objects.get_or_create(
                nimi=data['nimi'],
                lajike=data.get('lajike', ''),
                defaults=data,
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✅ {obj}'))
            else:
                self.stdout.write(f'  ⏭️  {obj} (oli jo)')

        self.stdout.write(self.style.SUCCESS(
            f'\nValmis! Lisätty {created_count} uutta kasvilajia.'
        ))
