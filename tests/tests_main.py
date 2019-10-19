import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ourchive_app.api.models import User

class ApiUserTests(APITestCase):

    @pytest.mark.django_db
    def test_my_user(self):
        me = User.objects.get(username='me')
        assert me.is_superuser

