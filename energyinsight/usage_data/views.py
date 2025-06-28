from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.db.models import Q

# SPA entrypoint
def SPA(request):
    return render(request, 'usage_data/spa.html')

# index
def index(request):
    return render(request, 'usage_data/index.html')

# about, versions and installed packages
def about(request):
    return render(request, 'usage_data/about.html')

# admin credentials
def admin_credentials(request):
    return render(request, 'usage_data/admin_credentials.html')

# LIST view - usage data
class UsageDataList(ListView):
    model = RenewableEnergyUsage
    context_object_name = 'master_usagedata'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country_filter = self.kwargs.get('country')
        source_filter = self.kwargs.get('source')

        if country_filter:
            context['master_usagedata'] = RenewableEnergyUsage.objects.filter(
                country__name__iexact=country_filter
            ).order_by('energy_source__name', '-year')
        elif source_filter:
            context['master_usagedata'] = RenewableEnergyUsage.objects.filter(
                energy_source__name__iexact=source_filter
            ).order_by('country__name', '-year')
        else:
            context['master_usagedata'] = RenewableEnergyUsage.objects.all().order_by('country__name', 'energy_source__name', '-year')

        context['selected_country'] = country_filter
        context['selected_source'] = source_filter
        return context

    def get_template_names(self):
        return 'usage_data/list.html'

# Countries
def countries(request):
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            country_id = request.POST.get('delete_id')
            Country.objects.filter(id=country_id).delete()
            return HttpResponseRedirect('/countries')  
        else:
            form = CountryForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/countries')
    else:
        form = CountryForm()

    countries = Country.objects.all().order_by('name')
    return render(request, 'usage_data/countries.html', {'form': form, 'countries': countries})

# Energy Sources
def sources(request):
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            source_id = request.POST.get('delete_id')
            EnergySource.objects.filter(id=source_id).delete()
            return HttpResponseRedirect('/sources')
        else:
            form = EnergySourceForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/sources')
    else:
        form = EnergySourceForm()

    sources = EnergySource.objects.all().order_by('name')
    return render(request, 'usage_data/sources.html', {'form': form, 'sources': sources})

# Detail view - usage data
class UsageDataDetail(DetailView):
    model = RenewableEnergyUsage
    context_object_name = 'usage_data'
    template_name = 'usage_data/usagedata.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
# DELETE view - usage data
class UsageDataDelete(DeleteView):
    model = RenewableEnergyUsage
    success_url = "/"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

# UPDATE view - usage data
class UsageDataUpdate(UpdateView):
    model = RenewableEnergyUsage
    form_class = UsageDataForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('usage_detail', kwargs={'pk': self.object.pk})
        
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

# CREATE view - usage data
class UsageDataCreate(CreateView):
    model = RenewableEnergyUsage
    template_name = 'usage_data/create_usagedata.html'
    form_class = UsageDataForm

    def get_success_url(self):
        return reverse_lazy('usage_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

# Search view - usage data ('household_id', 'country', 'energy source')
class UsageSearchView(ListView):
    model = RenewableEnergyUsage
    template_name = 'usage_data/search_results.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return RenewableEnergyUsage.objects.filter(
            Q(household_id__icontains=query) |
            Q(country__name__icontains=query) |
            Q(energy_source__name__icontains=query)
        ).order_by('household_id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context