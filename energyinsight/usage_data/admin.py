from django.contrib import admin
from .models import *

class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region')
    list_filter = ('region',)
    search_fields = ('name',)

class EnergySourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class IncomeLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'level')
    search_fields = ('level',)

class UrbanRuralAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')
    search_fields = ('type',)

class RenewableEnergyUsageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'household_id', 'country', 'energy_source',
        'monthly_usage_kwh', 'year', 'household_size',
        'income_level', 'urban_rural', 'adoption_year',
        'subsidy_received', 'cost_savings_usd'
    )
    list_filter = (
        'country__region', 'country', 'energy_source',
        'income_level', 'urban_rural', 'subsidy_received', 'year'
    )
    search_fields = ('household_id', 'country__name', 'energy_source__name')

admin.site.register(Region, RegionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(EnergySource, EnergySourceAdmin)
admin.site.register(IncomeLevel, IncomeLevelAdmin)
admin.site.register(UrbanRural, UrbanRuralAdmin)
admin.site.register(RenewableEnergyUsage, RenewableEnergyUsageAdmin)
