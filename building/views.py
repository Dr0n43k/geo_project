from .models import Building
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import BuildingSerializer
from django.contrib.gis.measure import D
import json
from django.contrib.gis.geos import Point
from rest_framework import status
from django.contrib.gis.db.models.functions import Transform

class BuildingData(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    def list(self, *args, **kwargs):
        queryset = self.queryset
        min_area = self.request.GET.get('min')
        max_area = self.request.GET.get('max')
        longitude = self.request.GET.get('longitude')
        latitude = self.request.GET.get('latitude')
        distance = self.request.GET.get('distance')
        if not (longitude is None and latitude is None and distance is None):
            try:
                float(longitude)
                float(latitude)
                distance = float(distance)
            except:
                return Response({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)
            point = f'POINT({longitude} {latitude})'
            queryset = queryset.filter(geom__distance_lte=(point, D(m=distance)))
        if max_area is None and min_area is None:
            serializer = self.get_serializer(queryset, many=True)
            values = serializer.data
            return Response(values)
        if max_area is None:
            try:
                min_area = float(min_area)
            except:
                return Response({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)
            values = [{"id": i['id'], "address": i['address'], "geom": list(i['geom'][0]),
                       "type": type(i['geom']).__name__}
                      for i in queryset.annotate(geom1=Transform('geom', 27700, clone=False)).values()
                      if i['geom1'].area >= min_area]
        elif min_area is None:
            try:
                max_area = float(max_area)
            except:
                return Response({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)
            values = [{"id": i['id'], "address": i['address'], "geom": list(i['geom'][0]),
                       "type":type(i['geom']).__name__}
                      for i in queryset.annotate(geom1=Transform('geom', 27700, clone=False)).values()
                      if i['geom1'].area <= max_area]
        else:
            try:
                max_area = float(max_area)
                min_area = float(min_area)
            except:
                return Response({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)
            values = [{"id": i['id'], "address": i['address'], "geom": list(i['geom'][0]),
                       "type": type(i['geom']).__name__}
                      for i in queryset.annotate(geom1=Transform('geom', 27700, clone=False)).values()
                      if min_area <= i['geom1'].area <= max_area]
        #ужасный костыль
        geojson = {"type": "FeatureCollection", "features": [{"id": i['id'], "type": "Feature",
        "geometry": {"type": i['type'], "coordinates": [i['geom']], "properties": {"address": i['address']}}}
        for i in values]}
        return Response(geojson)
