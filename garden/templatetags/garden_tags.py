"""Puutarhapäiväkirjan template-tagit."""
from django import template

register = template.Library()

KUUKAUDET = [
    '', 'tammi', 'helmi', 'maalis', 'huhti', 'touko', 'kesä',
    'heinä', 'elo', 'syys', 'loka', 'marras', 'joulu'
]


@register.filter
def kk_nimi(numero):
    """Muuttaa kuukausinumeron (1-12) suomenkieliseksi nimeksi."""
    try:
        return KUUKAUDET[int(numero)]
    except (ValueError, IndexError):
        return numero
