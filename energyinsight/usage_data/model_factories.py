import factory
from random import randint, choice
from .models import *

class RegionFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Region{n}")

    class Meta:
        model = Region

class CountryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Country{n}")
    region = factory.SubFactory(RegionFactory)

    class Meta:
        model = Country

class EnergySourceFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"EnergySource{n}")
    
    class Meta:
        model = EnergySource
        
class IncomeLevelFactory(factory.django.DjangoModelFactory):
    level = factory.Sequence(lambda n: f"IncomeLevel{n}") 
    
    class Meta:
        model = IncomeLevel

class UrbanRuralFactory(factory.django.DjangoModelFactory):
    type = factory.Sequence(lambda n: f"UrbanRuralType{n}") 
    
    class Meta:
        model = UrbanRural

class UsageDataFactory(factory.django.DjangoModelFactory):
    household_id = factory.Sequence(lambda n: f"H{n:05}")
    country = factory.SubFactory(CountryFactory)
    energy_source = factory.SubFactory(EnergySourceFactory)
    monthly_usage_kwh = factory.LazyFunction(lambda: round(randint(100, 2000) + randint(0, 99)/100, 2))
    year = factory.LazyFunction(lambda: randint(2000, 2025))
    household_size = factory.LazyFunction(lambda: randint(1, 6))
    income_level = factory.SubFactory(IncomeLevelFactory)
    urban_rural = factory.SubFactory(UrbanRuralFactory)
    adoption_year = factory.LazyFunction(lambda: randint(1990, 2020))
    subsidy_received = factory.LazyFunction(lambda: choice(['Yes', 'No']))
    cost_savings_usd = factory.LazyFunction(lambda: round(randint(0, 1000) + randint(0, 99)/100, 2))

    class Meta:
        model = RenewableEnergyUsage
