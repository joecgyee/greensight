import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status

from .model_factories import *
from .serializers import *
from .api import *
from .models import *

class ModelFactoryTests(TestCase):
    def setUp(self):
        self.usage_data = UsageDataFactory()
    
    def test_usage_data_creation(self):
        self.assertIsNotNone(self.usage_data.household_id)
        self.assertIsNotNone(self.usage_data.country)
        self.assertIsNotNone(self.usage_data.energy_source)
        self.assertTrue(100 <= self.usage_data.monthly_usage_kwh <= 2000)
        self.assertTrue(2000 <= self.usage_data.year <= 2025)
        self.assertTrue(1 <= self.usage_data.household_size <= 6)
        self.assertIn(self.usage_data.subsidy_received, ['Yes', 'No'])
        self.assertTrue(0 <= self.usage_data.cost_savings_usd <= 1000)

class SerializerTests(TestCase):
    def setUp(self):
        self.usage_data = UsageDataFactory()
        self.serializer = UsageDataSerializer(instance=self.usage_data)
    
    def test_usage_data_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {
            'household_id', 'country', 'energy_source', 'monthly_usage_kwh', 
            'year', 'household_size', 'income_level', 'urban_rural', 
            'adoption_year', 'subsidy_received', 'cost_savings_usd'
        })
    
    def test_usage_data_serializer_validation(self):
        data = {
            'household_id': 'H12345',
            'country_id': self.usage_data.country.id,
            'energy_source_id': self.usage_data.energy_source.id,
            'monthly_usage_kwh': 500.50,
            'year': 2023,
            'household_size': 4,
            'income_level_id': self.usage_data.income_level.id,
            'urban_rural_id': self.usage_data.urban_rural.id,
            'adoption_year': 2020,
            'subsidy_received': 'Yes',
            'cost_savings_usd': 250.75
        }
        serializer = UsageDataSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_country_serializer(self):
        country = CountryFactory()
        serializer = CountrySerializer(country)
        self.assertIn('name', serializer.data)
        self.assertIn('region', serializer.data)

class APITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up data for the whole TestCase (runs once)"""
        # Create test data that won't be modified during tests
        cls.region = RegionFactory()
        cls.country = CountryFactory(region=cls.region)
        cls.energy_source = EnergySourceFactory()
        cls.income_level = IncomeLevelFactory()
        cls.urban_rural = UrbanRuralFactory()
        
        # Create exactly 2 usage data instances
        cls.usage_data1 = UsageDataFactory(
            country=cls.country,
            energy_source=cls.energy_source,
            income_level=cls.income_level,
            urban_rural=cls.urban_rural
        )
        cls.usage_data2 = UsageDataFactory(
            country=cls.country,
            energy_source=cls.energy_source,
            income_level=cls.income_level,
            urban_rural=cls.urban_rural
        )

    def setUp(self):
        """Set up for each individual test (runs before each test)"""
        pass

    def test_usage_data_list_api(self):
        url = reverse('usage_list_api')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check the response structure for paginated data
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)
        
        # Get all household_ids in the response
        response_household_ids = [item['household_id'] for item in response.data['results']]
        
        # Verify our test items are present
        self.assertIn(self.usage_data1.household_id, response_household_ids)
        self.assertIn(self.usage_data2.household_id, response_household_ids)
        
        # Verify the count matches
        self.assertEqual(response.data['count'], 2)

    def test_usage_data_by_pk_api(self):
        url = reverse('usage_detail_pk_api', kwargs={'pk': self.usage_data1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['household_id'], self.usage_data1.household_id)
    
    def test_usage_data_by_household_id_api(self):
        url = reverse('usage_detail_householdID_api', kwargs={'household_id': self.usage_data1.household_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['household_id'], self.usage_data1.household_id)
    
    def test_usage_data_by_country_api(self):
        url = reverse('usage_by_country_api', kwargs={'country_name': self.country.name})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)
    
    def test_usage_data_by_source_api(self):
        url = reverse('usage_by_source_api', kwargs={'source_name': self.energy_source.name})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)
    
    def test_energy_source_list_api(self):
        url = reverse('source_list_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_country_list_api(self):
        url = reverse('country_list_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_total_savings_by_country_api(self):
        url = reverse('total_savings_country_api', kwargs={'country_name': self.country.name})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
    
    def test_total_savings_by_country_api_invalid_country(self):
        url = reverse('total_savings_country_api', kwargs={'country_name': 'NonexistentCountry'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_usage_data_create_api(self):
        url = reverse('usage_list_api')
        data = {
            'household_id': 'H99999',
            'country_id': self.country.id,
            'energy_source_id': self.energy_source.id,
            'monthly_usage_kwh': 750.25,
            'year': 2023,
            'household_size': 3,
            'income_level_id': self.usage_data1.income_level.id,
            'urban_rural_id': self.usage_data1.urban_rural.id,
            'adoption_year': 2019,
            'subsidy_received': 'No',
            'cost_savings_usd': 300.50
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['household_id'], 'H99999')
    
    def test_usage_data_update_api(self):
        url = reverse('usage_detail_pk_api', kwargs={'pk': self.usage_data1.pk})
        data = {
            'household_id': self.usage_data1.household_id,
            'country_id': self.country.id,
            'energy_source_id': self.energy_source.id,
            'monthly_usage_kwh': 850.75,
            'year': 2023,
            'household_size': 4,
            'income_level_id': self.usage_data1.income_level.id,
            'urban_rural_id': self.usage_data1.urban_rural.id,
            'adoption_year': 2019,
            'subsidy_received': 'Yes',
            'cost_savings_usd': 350.25
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['monthly_usage_kwh']), 850.75)
    
    def test_usage_data_delete_api(self):
        url = reverse('usage_detail_pk_api', kwargs={'pk': self.usage_data1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RenewableEnergyUsage.objects.filter(pk=self.usage_data1.pk).exists())

class TotalSavingsByCountryTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up data for the whole TestCase (runs once)"""
        # Create unique instances first
        cls.region = RegionFactory()
        cls.country = CountryFactory(region=cls.region)
        cls.energy_source1 = EnergySourceFactory()
        cls.energy_source2 = EnergySourceFactory()
        cls.income_level = IncomeLevelFactory()
        cls.urban_rural = UrbanRuralFactory()  
        
        # Create usage data with different cost savings
        UsageDataFactory.create_batch(
            3,
            country=cls.country,
            energy_source=cls.energy_source1,
            income_level=cls.income_level,
            urban_rural=cls.urban_rural,
            cost_savings_usd=100.00
        )
        UsageDataFactory.create_batch(
            2,
            country=cls.country,
            energy_source=cls.energy_source2,
            income_level=cls.income_level,
            urban_rural=cls.urban_rural,
            cost_savings_usd=200.00
        )

    def setUp(self):
        """Set up for each individual test (runs before each test)"""
        self.view = TotalSavingsByCountry.as_view()
        self.factory = APIRequestFactory()
    
    def test_total_savings_calculation(self):
        request = self.factory.get(f'/api/costsavings/{self.country.name}/')
        response = self.view(request, country_name=self.country.name)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verify the sums are correct with floating-point tolerance
        for item in response.data:
            if item['energy_source']['id'] == self.energy_source1.id:
                self.assertAlmostEqual(item['total_cost_savings_usd'], 300.00, places=2)
            elif item['energy_source']['id'] == self.energy_source2.id:
                self.assertAlmostEqual(item['total_cost_savings_usd'], 400.00, places=2)