import pytest
#from api.urls import urlpatterns
import requests
#from rest_framework.test import APITestCase
#from api.models import User
import os
import logging

root = 'http://host.docker.internal:8000/'

#def test_01():

#    print(urlpatterns)
#    assert 2+2 == 4

@pytest.mark.parametrize("endpoint", ['users', 'works'])
def test_api_connect(endpoint):

    url = root + 'api/' + endpoint
    logging.info(url)
    response = requests.get(url)
    assert response.status_code == 200
    assert len(response.json()) > 0