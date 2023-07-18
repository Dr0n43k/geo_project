from django.contrib.gis.db import models
from rest_framework import serializers


def validation(value):
    if not value.valid:
        raise serializers.ValidationError(value.valid_reason)


class Building(models.Model):
    address = models.CharField(max_length=100)
    geom = models.GeometryField(srid=4326, validators=[validation])

