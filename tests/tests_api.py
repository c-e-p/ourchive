#
import pytest
import requests
import os
import logging

root = 'http://host.docker.internal:8000/'


def get_endpoints():

    url = root + 'api/'
    response = requests.get(url)
    urlpatterns = response.json()

    return list(urlpatterns)


def test_01():

    url = root + 'api/'
    response = requests.get(url)
    urlpatterns = response.json()

    logging.info(list(urlpatterns))


@pytest.mark.parametrize("endpoint", get_endpoints())
def test_api_connect(endpoint):

    url = root + 'api/' + endpoint

    response = requests.get(url)
    logging.info(endpoint)
    logging.info(response.json())
    assert response.status_code == 200
    assert response.json()['count'] is not None


def test_user_crud():

    url = root + 'api/'

    body = {

    }

    r = requests.post(url, body)