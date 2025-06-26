import os
import sys
import django
import csv
import json

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # This goes two levels up to the project root (same level as manage.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'energyinsight.settings')  
django.setup()

from usage_data.models import *
from django.db import connection

# Define helper to get or create related records
def get_or_create_model(model, **kwargs):
    obj, _ = model.objects.get_or_create(**kwargs)
    return obj

# Resets the auto-incrementing primary key (ID) for a given model in SQLite.
def reset_sqlite_sequence(model):
    table_name = model._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")

def main():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "Renewable_Energy_Usage_Sampled.csv"))

    RenewableEnergyUsage.objects.all().delete()
    reset_sqlite_sequence(RenewableEnergyUsage)

    Region.objects.all().delete()
    reset_sqlite_sequence(Region)

    Country.objects.all().delete()
    reset_sqlite_sequence(Country)

    EnergySource.objects.all().delete()
    reset_sqlite_sequence(EnergySource)

    IncomeLevel.objects.all().delete()
    reset_sqlite_sequence(IncomeLevel)

    UrbanRural.objects.all().delete()
    reset_sqlite_sequence(UrbanRural)

    output_json = []

    # Read CSV and insert into DB
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            region = get_or_create_model(Region, name=row['Region'].strip())
            country = get_or_create_model(Country, name=row['Country'].strip(), region=region)
            energy_source = get_or_create_model(EnergySource, name=row['Energy_Source'].strip())
            income_level = get_or_create_model(IncomeLevel, level=row['Income_Level'].strip())
            urban_rural = get_or_create_model(UrbanRural, type=row['Urban_Rural'].strip())

            usage = RenewableEnergyUsage.objects.create(
                household_id=row['Household_ID'].strip(),
                country=country,
                energy_source=energy_source,
                monthly_usage_kwh=float(row['Monthly_Usage_kWh']),
                year=int(row['Year']),
                household_size=int(row['Household_Size']),
                income_level=income_level,
                urban_rural=urban_rural,
                adoption_year=int(row['Adoption_Year']),
                subsidy_received=row['Subsidy_Received'].strip(),
                cost_savings_usd=float(row['Cost_Savings_USD'])
            )

            output_json.append({
                "household_id": usage.household_id,
                "country": usage.country.name,
                "region": usage.country.region.name,
                "energy_source": usage.energy_source.name,
                "monthly_usage_kwh": usage.monthly_usage_kwh,
                "year": usage.year,
                "household_size": usage.household_size,
                "income_level": usage.income_level.level,
                "urban_rural": usage.urban_rural.type,
                "adoption_year": usage.adoption_year,
                "subsidy_received": usage.subsidy_received,
                "cost_savings_usd": usage.cost_savings_usd
            })

    # Output to console as JSON
    print(json.dumps(output_json, indent=2))

if __name__ == "__main__":
    main()
