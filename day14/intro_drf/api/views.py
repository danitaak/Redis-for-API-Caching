# from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication
from django.core.cache import cache
from django.db.models import Q
from .serializers import *
from .models import *


# Create your views here.

class InstitutionsView(ListAPIView):
    queryset = Institutions.objects.all()
    serializer_class = InstitutionsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        institution_name = self.request.query_params.get('name', None)
        symbol_name =  self.request.query_params
        if institution_name:
                # queryset = queryset.filter(top_sellers__contains=[{'name': institution_name}])
            queryset = queryset.filter(
                Q(top_sellers__contains=[{'name': institution_name}]) |
                Q(top_buyers__contains=[{'name': institution_name}])
            )
            # return queryset
        for param, value in symbol_name.items():
            if param != 'name':
                queryset = queryset.filter(**{f"{param}__icontains": value})  # ** unpacks dictionary into keyword arguments. so that its keys and values are passed as keyword arguments to the function.
        return queryset


    def list(self, request):
        query_params = request.query_params.urlencode()
        cache_key = f'institution-trade-{query_params}'  # Define a unique cache key for this data
        # cache_key = self.request.get_full_path()
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset()  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response



class MetadataView(ListAPIView):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        metadata_name = self.request.query_params
        for param, value in metadata_name.items():
            queryset = queryset.filter(**{f"{param}__icontains": value}) # ** unpacks dictionary into keyword arguments. so that its keys and values are passed as keyword arguments to the function.
        return queryset

    def list(self, request):
        query_params = request.query_params.urlencode()
        cache_key = f'metadata-{query_params}'  # Define a unique cache key for this data
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset()  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response



class ReportsView(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        reports_name = self.request.query_params
        for param, value in reports_name.items():
            filter_reports = {f"{param}__icontains": value}
            # queryset = queryset.filter(**{f"{param}__icontains": value})
            queryset = queryset.filter(**filter_reports) # ** unpacks dictionary into keyword arguments. so that its keys and values are passed as keyword arguments to the function.
        return queryset

    def list(self, request):
        query_params = request.query_params.urlencode()
        cache_key = f'reports-{query_params}'  # Define a unique cache key for this data
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset()  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response

