import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.settings import api_settings
import requests
#from rest_framework.test import APITestCase
#from api.models import User
import os


def test_api_connect():
    response = requests.get('http://127.0.0.1:8000/api/users')
    assert response.status_code == 200
    assert len(response.json()) > 0