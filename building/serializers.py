from rest_framework_gis import serializers
from .models import Building


class BuildingSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        geo_field = 'geom'
        model = Building
        fields =['id', 'geom', 'address']