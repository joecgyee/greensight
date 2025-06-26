from rest_framework import serializers
from .models import *

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']

class CountrySerializer(serializers.ModelSerializer):
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(), write_only=True
    )
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Country
        fields = ['id', 'name', 'region_id', 'region']

    def create(self, validated_data):
        region_data = validated_data.pop('region')
        region, _ = Region.objects.get_or_create(**region_data)
        new_country = Country.objects.create(region=region, **validated_data)
        return new_country

class EnergySourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergySource
        fields = ['id', 'name']

class IncomeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeLevel
        fields = ['id', 'level']

class UrbanRuralSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrbanRural
        fields = ['id', 'type']

class UsageDataSerializer(serializers.ModelSerializer):
    # Used only for writing (input)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), write_only=True
    )
    energy_source_id = serializers.PrimaryKeyRelatedField(
        queryset=EnergySource.objects.all(), write_only=True
    )
    income_level_id = serializers.PrimaryKeyRelatedField(
        queryset=IncomeLevel.objects.all(), write_only=True
    )
    urban_rural_id = serializers.PrimaryKeyRelatedField(
        queryset=UrbanRural.objects.all(), write_only=True
    )

    # Used only for reading (output)
    country = CountrySerializer(read_only=True)
    energy_source = EnergySourceSerializer(read_only=True)
    income_level = IncomeLevelSerializer(read_only=True)
    urban_rural = UrbanRuralSerializer(read_only=True)    
    
    class Meta:
        model = RenewableEnergyUsage
        fields = [
            'household_id',
            'country_id', 'country',
            'energy_source_id', 'energy_source',
            'monthly_usage_kwh', 'year', 'household_size',
            'income_level_id', 'income_level',
            'urban_rural_id', 'urban_rural',
            'adoption_year', 'subsidy_received', 'cost_savings_usd'
        ]
    
    def update(self, instance, validated_data):    
        instance.household_id = validated_data.get('household_id', instance.household_id)
        instance.country = validated_data.get('country_id', instance.country)
        instance.energy_source = validated_data.get('energy_source_id', instance.energy_source)
        instance.monthly_usage_kwh = validated_data.get('monthly_usage_kwh', instance.monthly_usage_kwh)
        instance.year = validated_data.get('year', instance.year)
        instance.household_size = validated_data.get('household_size', instance.household_size)
        instance.income_level = validated_data.get('income_level_id', instance.income_level)
        instance.urban_rural = validated_data.get('urban_rural_id', instance.urban_rural)
        instance.adoption_year = validated_data.get('adoption_year', instance.adoption_year)
        instance.subsidy_received = validated_data.get('subsidy_received', instance.subsidy_received)
        instance.cost_savings_usd = validated_data.get('cost_savings_usd', instance.cost_savings_usd)

        instance.save()
        return instance
    
class UsageDataListSerializer(serializers.ModelSerializer):
    # Used only for writing (input)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), write_only=True
    )
    energy_source_id = serializers.PrimaryKeyRelatedField(
        queryset=EnergySource.objects.all(), write_only=True
    )
    income_level_id = serializers.PrimaryKeyRelatedField(
        queryset=IncomeLevel.objects.all(), write_only=True
    )
    urban_rural_id = serializers.PrimaryKeyRelatedField(
        queryset=UrbanRural.objects.all(), write_only=True
    )

    # Used only for reading (output)
    country = CountrySerializer(read_only=True)
    energy_source = EnergySourceSerializer(read_only=True)
    income_level = IncomeLevelSerializer(read_only=True)
    urban_rural = UrbanRuralSerializer(read_only=True)    
    
    class Meta:
        model = RenewableEnergyUsage
        fields = [
            'household_id',
            'country_id', 'country',
            'energy_source_id', 'energy_source',
            'monthly_usage_kwh', 'year', 'household_size',
            'income_level_id', 'income_level',
            'urban_rural_id', 'urban_rural',
            'adoption_year', 'subsidy_received', 'cost_savings_usd'
        ]

    def create(self, validated_data):
        country = validated_data.pop('country_id')
        energy_source = validated_data.pop('energy_source_id')
        income_level = validated_data.pop('income_level_id')
        urban_rural = validated_data.pop('urban_rural_id')

        new_usage_data = RenewableEnergyUsage.objects.create(
            country=country,
            energy_source=energy_source,
            income_level=income_level,
            urban_rural=urban_rural,
            **validated_data
        )
        return new_usage_data

class TotalSavingsSerializer(serializers.Serializer):
    energy_source = EnergySourceSerializer()
    total_cost_savings = serializers.FloatField()
