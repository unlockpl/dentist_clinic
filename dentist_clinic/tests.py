from django.test import TestCase, Client
import pytest
from django.urls import reverse, reverse_lazy


# Create your tests here.


def test_login():
    client = Client()
    response = client.get(reverse_lazy("login"))
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_login_with_user(user, user_data):
#     client = Client()
#     client.force_login(user)
#     user_data.user = user
#     response = client.get(reverse('login'))
#     assert response.status_code == 200

