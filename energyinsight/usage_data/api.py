from rest_framework import generics, mixins
from rest_framework.response import Response
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *

class UsageDataByPK(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = RenewableEnergyUsage.objects.all()
    serializer_class = UsageDataSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class UsageDataByHouseholdID(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UsageDataSerializer
    lookup_field = 'household_id'
    lookup_url_kwarg = 'household_id'
    
    def get_queryset(self):
        return RenewableEnergyUsage.objects.all()
    
    def get_object(self):
        household_id = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(RenewableEnergyUsage, household_id=household_id)

class UsageDataList(generics.ListCreateAPIView):
    queryset = RenewableEnergyUsage.objects.all()
    serializer_class = UsageDataListSerializer 

class EnergySourceList(generics.ListAPIView):
    queryset = EnergySource.objects.all()
    serializer_class = EnergySourceSerializer

class CountryList(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class UsageDataByCountry(generics.ListAPIView):
    serializer_class = UsageDataSerializer

    def get_queryset(self):
        country_name = self.kwargs["country_name"]
        return RenewableEnergyUsage.objects.filter(country__name__iexact=country_name)

class UsageDataBySource(generics.ListAPIView):
    serializer_class = UsageDataSerializer

    def get_queryset(self):
        source_name = self.kwargs["source_name"]
        return RenewableEnergyUsage.objects.filter(energy_source__name__iexact=source_name)

class TotalSavingsByCountry(generics.ListAPIView):
    serializer_class = TotalSavingsSerializer

    def get_queryset(self):
        # Not used directly, but required by DRF
        return []

    def list(self, request, *args, **kwargs):
        country_name = self.kwargs.get('country_name')
        try:
            country = Country.objects.get(name__iexact=country_name)
        except Country.DoesNotExist:
            return Response(
                {"error": f"Country '{country_name}' not found."},
                status=404
            )

        # Group by energy_source and calculate total cost savings
        usage_data = (
            RenewableEnergyUsage.objects
            .filter(country=country)
            .values('energy_source')
            .annotate(total_cost_savings_usd=Sum('cost_savings_usd'))
        )

        # Prepare data using full EnergySourceSerializer
        result = []
        for item in usage_data:
            try:
                energy_source = EnergySource.objects.get(pk=item['energy_source'])
            except EnergySource.DoesNotExist:
                continue
            result.append({
                'energy_source': EnergySourceSerializer(energy_source).data,
                'total_cost_savings_usd': item['total_cost_savings_usd']
            })

        return Response(result)