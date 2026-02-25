"""Puutarhapäiväkirjan tietomallit."""
from django.db import models


class PlantSpecies(models.Model):
    """Kasvilaji Nelson Gardenin tuotetietojen mukaan."""

    KASVUPAIKKA_CHOICES = [
        ('aurinko', 'Aurinko'),
        ('puolivarjo', 'Puolivarjo'),
        ('varjo', 'Varjo'),
    ]

    KUUKAUSI_CHOICES = [(i, i) for i in range(1, 13)]

    nelson_garden_id = models.CharField(
        'Nelson Garden ID', max_length=20, blank=True, default=''
    )
    nimi = models.CharField('Nimi', max_length=100)
    lajike = models.CharField('Lajike', max_length=100, blank=True, default='')
    kategoria = models.CharField('Kategoria', max_length=50)
    kuvaus = models.TextField('Kuvaus', blank=True, default='')
    kasvatusohje = models.TextField('Kasvatusohje', blank=True, default='')

    kylvo_alku_kk = models.IntegerField('Kylvö alkaa (kk)', choices=KUUKAUSI_CHOICES)
    kylvo_loppu_kk = models.IntegerField('Kylvö päättyy (kk)', choices=KUUKAUSI_CHOICES)
    sato_alku_kk = models.IntegerField('Sato alkaa (kk)', choices=KUUKAUSI_CHOICES)
    sato_loppu_kk = models.IntegerField('Sato päättyy (kk)', choices=KUUKAUSI_CHOICES)

    itamisaika_min_pv = models.IntegerField('Itämisaika min (pv)', default=7)
    itamisaika_max_pv = models.IntegerField('Itämisaika max (pv)', default=14)
    korkeus_cm = models.IntegerField('Korkeus (cm)', blank=True, null=True)
    kasvupaikka = models.CharField(
        'Kasvupaikka', max_length=20, choices=KASVUPAIKKA_CHOICES, default='aurinko'
    )
    siemenia_pakkauksessa = models.IntegerField(
        'Siemeniä pakkauksessa', blank=True, null=True
    )
    nelson_garden_url = models.URLField('Nelson Garden URL', blank=True, default='')

    class Meta:
        verbose_name = 'Kasvilaji'
        verbose_name_plural = 'Kasvilajit'
        ordering = ['kategoria', 'nimi']

    def __str__(self):
        if self.lajike:
            return f"{self.nimi} '{self.lajike}'"
        return self.nimi

    def kylvo_kuukaudet(self):
        """Palauttaa listan kylvökuukausista."""
        if self.kylvo_alku_kk <= self.kylvo_loppu_kk:
            return list(range(self.kylvo_alku_kk, self.kylvo_loppu_kk + 1))
        return list(range(self.kylvo_alku_kk, 13)) + list(range(1, self.kylvo_loppu_kk + 1))

    def sato_kuukaudet(self):
        """Palauttaa listan satokuukausista."""
        if self.sato_alku_kk <= self.sato_loppu_kk:
            return list(range(self.sato_alku_kk, self.sato_loppu_kk + 1))
        return list(range(self.sato_alku_kk, 13)) + list(range(1, self.sato_loppu_kk + 1))


class MyGarden(models.Model):
    """Oma viljelymerkintä."""

    TILA_CHOICES = [
        ('odottaa', '🌑 Odottaa kylvöä'),
        ('kylvetty', '🌱 Kylvetty'),
        ('itanyt', '🌿 Itänyt'),
        ('kasvaa', '💚 Kasvaa hyvin'),
        ('sadonkorjuu', '🍅 Sadonkorjuussa'),
        ('paattynyt', '✅ Päättynyt'),
    ]

    kasvilaji = models.ForeignKey(
        PlantSpecies, on_delete=models.CASCADE,
        verbose_name='Kasvilaji', related_name='viljelyt'
    )
    kasvupaikka = models.CharField(
        'Kasvupaikka', max_length=100, blank=True, default='',
        help_text='Esim. parvekelaatikko, kasvihuone, palsta'
    )
    tila = models.CharField(
        'Tila', max_length=20, choices=TILA_CHOICES, default='odottaa'
    )
    kylvopaiva = models.DateField('Kylvöpäivä', blank=True, null=True)
    muistiinpanot = models.TextField('Muistiinpanot', blank=True, default='')
    lisatty = models.DateTimeField('Lisätty', auto_now_add=True)

    class Meta:
        verbose_name = 'Viljelymerkintä'
        verbose_name_plural = 'Viljelymerkinnät'
        ordering = ['-lisatty']

    def __str__(self):
        return f"{self.kasvilaji} — {self.get_tila_display()}"

    def arvioitu_sato(self):
        """Laskee arvioidun sadon alkamispäivän kylvöpäivästä."""
        if self.kylvopaiva and self.kasvilaji:
            from datetime import timedelta
            kasvuaika = (self.kasvilaji.sato_alku_kk - self.kasvilaji.kylvo_alku_kk) * 30
            if kasvuaika <= 0:
                kasvuaika = 90  # oletusarvo
            return self.kylvopaiva + timedelta(days=kasvuaika)
        return None


class GardenNote(models.Model):
    """Kasvatushavainto."""

    kasvi = models.ForeignKey(
        MyGarden, on_delete=models.CASCADE,
        verbose_name='Viljelymerkintä', related_name='havainnot'
    )
    paivamaara = models.DateField('Päivämäärä')
    havainto = models.TextField('Havainto')

    class Meta:
        verbose_name = 'Havainto'
        verbose_name_plural = 'Havainnot'
        ordering = ['-paivamaara']

    def __str__(self):
        return f"{self.paivamaara} — {self.havainto[:50]}"
