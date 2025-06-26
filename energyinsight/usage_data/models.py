from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='countries')

    def __str__(self):
        return self.name

class EnergySource(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)

    def __str__(self):
        return self.name

class IncomeLevel(models.Model):
    level = models.CharField(max_length=10, unique=True, null=False, blank=False)  # e.g., Low, Middle, High

    def __str__(self):
        return self.level

class UrbanRural(models.Model):
    type = models.CharField(max_length=10, unique=True, null=False, blank=False)  # Urban or Rural

    def __str__(self):
        return self.type

class RenewableEnergyUsage(models.Model):
    SUBSIDY_CHOICES = [('Yes', 'Yes'), ('No', 'No')]

    household_id = models.CharField(max_length=10, unique=True, null=False, blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='usages')
    energy_source = models.ForeignKey(EnergySource, on_delete=models.SET_NULL, null=True, related_name='usages')
    monthly_usage_kwh = models.FloatField()
    year = models.PositiveIntegerField()
    household_size = models.PositiveIntegerField()
    income_level = models.ForeignKey(IncomeLevel, on_delete=models.SET_NULL, null=True)
    urban_rural = models.ForeignKey(UrbanRural, on_delete=models.SET_NULL, null=True)
    adoption_year = models.PositiveIntegerField()
    subsidy_received = models.CharField(max_length=3, choices=SUBSIDY_CHOICES)
    cost_savings_usd = models.FloatField()

    def __str__(self):
        return f"{self.household_id} - {self.country.name} - {self.energy_source.name}"
