from django import forms
from django.forms import ModelForm
from .models import *

# Country
class CountryForm(ModelForm):
    class Meta:
        model = Country
        fields = ['name', 'region']
        
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        region = cleaned_data.get("region")

        if region not in Region.objects.all():
            raise forms.ValidationError("Selected region is not valid.")

        return (cleaned_data)

# Energy Source
class EnergySourceForm(ModelForm):
    class Meta:
        model = EnergySource
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter energy source name'}),
        }

# Usage Data
class UsageDataForm(ModelForm):
    class Meta:
        model = RenewableEnergyUsage
        fields = ['household_id', 'country', 'energy_source', 'monthly_usage_kwh', 
                  'year', 'household_size', 'income_level', 'urban_rural', 
                  'adoption_year', 'subsidy_received', 'cost_savings_usd']

    def clean(self):
        cleaned_data = super().clean()

        country = cleaned_data.get("country")
        energy_source = cleaned_data.get("energy_source")
        monthly_usage_kwh = cleaned_data.get("monthly_usage_kwh")
        year = cleaned_data.get("year")
        household_size = cleaned_data.get("household_size")
        income_level = cleaned_data.get("income_level")
        urban_rural = cleaned_data.get("urban_rural")
        adoption_year = cleaned_data.get("adoption_year")
        subsidy_received = cleaned_data.get("subsidy_received")
        cost_savings_usd = cleaned_data.get("cost_savings_usd")

        if country not in Country.objects.all():
            raise forms.ValidationError("Invalid country.")
        if energy_source not in EnergySource.objects.all():
            raise forms.ValidationError("Invalid energy source.")
        if monthly_usage_kwh is None or monthly_usage_kwh <= 0:
            raise forms.ValidationError("Monthly usage must be greater than 0 and cannot be empty.")
        if year is None or year <= 0:
            raise forms.ValidationError("Year must be positive integer and cannot be empty.")
        if household_size is None or household_size <= 0:
            raise forms.ValidationError("Household size must be greater than 0 and cannot be empty.")
        if income_level not in IncomeLevel.objects.all():
            raise forms.ValidationError("Income level must be Low, Middle or High.")
        if urban_rural not in UrbanRural.objects.all():
            raise forms.ValidationError("Invalid urban_rural type.")
        if adoption_year is None or adoption_year <= 0:
            raise forms.ValidationError("Adoption year must be positive integer and cannot be empty.")
        if subsidy_received not in dict(RenewableEnergyUsage.SUBSIDY_CHOICES):
            raise forms.ValidationError("This must be 'Yes' or 'No'.")
        if cost_savings_usd <= 0:
            raise forms.ValidationError("Cost savings must be greater than 0.")
        
        return (cleaned_data)
