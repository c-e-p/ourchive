import pytest
from api.urls import urlpatterns
import requests
#from rest_framework.test import APITestCase
#from api.models import User
import os


def test_01():

    print(urlpatterns)
    assert 2+2 == 4

@pytest.mark.parametrize("endpoint", ['users', 'works'])
def test_api_connect(endpoint):
    response = requests.get('http://127.0.0.1:8000/api/'+endpoint)
    assert response.status_code == 200
    assert len(response.json()) > 0