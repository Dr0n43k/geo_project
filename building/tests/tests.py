from django.test import TestCase
import random
import requests


class AreaFilterTest(TestCase):
    url = "http://127.0.0.1:8000/api/building" #enter your url here

    def test_values(self):
        random_value = random.uniform(0.0, 100000.0)
        max_area = random_value
        min_area = random_value
        request = requests.get(url=self.url+f"?min={min_area}&max={max_area}")
        self.assertEqual(200, request.status_code)

    def test_none(self):
        request = requests.get(url=self.url)
        self.assertEqual(200, request.status_code)

    def test_incorrect_value(self):
        max_area = "dsad"
        min_area = "random_value"
        request = requests.get(url=self.url + f"?min={min_area}&max={max_area}")
        self.assertEqual(400, request.status_code)

    def test_only_max(self):
        random_value = random.uniform(0.0, 100000.0)
        max_area = random_value
        request = requests.get(url=self.url + f"?max={max_area}")
        self.assertEqual(200, request.status_code)

    def test_only_min(self):
        random_value = random.uniform(0.0, 100000.0)
        min_area = random_value
        request = requests.get(url=self.url + f"?min={min_area}")
        self.assertEqual(200, request.status_code)


class DistanceFilterTest(TestCase):
    url = "http://127.0.0.1:8000/api/building" #enter your url here

    def test_values(self):
        longitude = random.uniform(0.0, 180.0)
        latitude = random.uniform(0.0, 90.0)
        distance = random.uniform(0.0, 100000.0)
        request = requests.get(url=self.url + f"?distance={distance}&latitude={latitude}&longitude={longitude}")
        self.assertEqual(200, request.status_code)

    def test_not_longitude(self):
        latitude = random.uniform(0.0, 90.0)
        distance = random.uniform(0.0, 100000000.0)
        request = requests.get(url=self.url + f"?distance={distance}&latitude={latitude}")
        self.assertEqual(400, request.status_code)

    def test_not_latitude(self):
        longitude = random.uniform(0.0, 180.0)
        distance = random.uniform(0.0, 100000000.0)
        request = requests.get(url=self.url + f"?distance={distance}&longitude{longitude}")
        self.assertEqual(400, request.status_code)

    def test_not_distance(self):
        longitude = random.uniform(0.0, 180.0)
        latitude = random.uniform(0.0, 90.0)
        request = requests.get(url=self.url + f"?latitude={latitude}&longitude{longitude}")
        self.assertEqual(400, request.status_code)

    def test_none(self):
        request = requests.get(url=self.url)
        self.assertEqual(200, request.status_code)

    def test_values_incorrect(self):
        longitude = "random.uniform(0.0, 180.0)"
        latitude = "random.uniform(0.0, 90.0)"
        distance = "random.uniform(0.0, 100000000.0)"
        request = requests.get(url=self.url + f"?distance={distance}&latitude={latitude}&longitude{longitude}")
        self.assertEqual(400, request.status_code)



