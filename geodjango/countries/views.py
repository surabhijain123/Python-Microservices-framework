from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Country
from .serializers import CountrySerializer

import requests
import geojson
from shapely.geometry import shape


def add_data():
    url = 'https://datahub.io/core/geo-countries/r/countries.geojson'
    r = requests.get(url, allow_redirects=True)
    values = geojson.loads(r.content)['features']
    for value in values:
        geometry = value['geometry']['type']
        if geometry == 'Polygon':
            g2 = shape({'type': 'MultiPolygon', 'coordinates': [value['geometry']['coordinates']]})
        else:
            g2 = shape(value['geometry'])
        value_data = {"admin": value['properties']['ADMIN'],
                      "iso_a3": value['properties']['ISO_A3'],
                      "geometry_type": geometry,
                      "coordinates": str(g2)}
        serializer = CountrySerializer(data=value_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()


class CountryViewSet(viewsets.ViewSet):

    def list(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CountrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def upload(self, request):
        add_data()
        return Response({'status': 'Data uploaded'}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        country = Country.objects.get(id=pk)
        serializer = CountrySerializer(country)
        return Response(serializer.data)

    def update(self, request, pk=None):
        country = Country.objects.get(id=pk)
        serializer = CountrySerializer(instance=country, data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        country = Country.objects.get(id=pk)
        country.delete()
        return Response(status.HTTP_204_NO_CONTENT)

    def matching_names(self, request, pk=None):
        countries = Country.objects.filter(admin=pk)
        data = {'results': []}
        for country in countries:
            serializer = CountrySerializer(country)
            data['results'].append(serializer.data)
        return Response(data)

    def intersecting(self, request, pk=None):
        countries = Country.objects.filter(admin=pk)
        data = {'results': []}
        for country in countries:
            intersections = Country.objects.filter(coordinates__intersects=country.coordinates)
            for value in intersections:
                serializer = CountrySerializer(value)
                data['results'].append(serializer.data)
        return Response(data)
