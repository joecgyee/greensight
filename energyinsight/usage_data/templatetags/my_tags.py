import datetime
from django import template
from usage_data.models import *

register = template.Library()

@register.simple_tag
def todays_date():
    return datetime.datetime.now().strftime("%d %b, %Y")

@register.inclusion_tag('partials/energy_source_list.html')
def energy_sources():
    return {'sources': EnergySource.objects.all()}

@register.inclusion_tag('partials/country_list.html')
def countries():
    return {'countries': Country.objects.all()}
