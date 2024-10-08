from .views import *
from django.urls import path


urlpatterns = [
    path('get-institution-trade', InstitutionsView.as_view(), name='get-institution-trade'),
    path('get-metadata', MetadataView.as_view(), name='get-metadata'),
    path('get-reports', ReportsView.as_view(), name='get-reports'),
]
