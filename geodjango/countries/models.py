from django.contrib.gis.db import models


class Country(models.Model):
    admin = models.CharField(max_length=200)
    iso_a3 = models.CharField(max_length=200)
    geometry_type = models.CharField(max_length=200)
    coordinates = models.MultiPolygonField()