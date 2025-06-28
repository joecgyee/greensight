from django.urls import include, path
from . import views
from . import api

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('admin_credentials/', views.admin_credentials, name='admin_credentials'),
    path('search/', views.UsageSearchView.as_view(), name='usage_search'),

    path('list/', views.UsageDataList.as_view(), name='usage_all'),
    path('list/country/<str:country>/', views.UsageDataList.as_view(), name='usage_by_country'),
    path('list/source/<str:source>/', views.UsageDataList.as_view(), name='usage_by_source'),

    path('countries/', views.countries, name='countries'),
    path('sources/', views.sources, name='sources'),
    
    path('usagedata/<int:pk>/', views.UsageDataDetail.as_view(), name='usage_detail'),
    path('usagedata/delete/<int:pk>/', views.UsageDataDelete.as_view(), name='usage_delete'),
    path('usagedata/update/<int:pk>/', views.UsageDataUpdate.as_view(), name='usage_update'),
    path('usagedata/create/', views.UsageDataCreate.as_view(), name='usage_create'),

    # APIs
    path('api/usagedata/', api.UsageDataList.as_view(), name='usage_list_api'), 
    path('api/usagedata/<int:pk>/', api.UsageDataByPK.as_view(), name='usage_detail_pk_api'),
    path('api/usagedata/hhid/<str:household_id>/', api.UsageDataByHouseholdID.as_view(), name='usage_detail_householdID_api'),
    path('api/usagedata/country/<str:country_name>/', api.UsageDataByCountry.as_view(), name='usage_by_country_api'),
    path('api/usagedata/source/<str:source_name>/', api.UsageDataBySource.as_view(), name='usage_by_source_api'),
    path('api/source/', api.EnergySourceList.as_view(), name='source_list_api'),
    path('api/country/', api.CountryList.as_view(), name='country_list_api'),
    path('api/costsavings/<str:country_name>/', api.TotalSavingsByCountry.as_view(), name='total_savings_country_api'),

    path('app/', views.SPA, name="spa"),

]
