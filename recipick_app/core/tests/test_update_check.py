"""
Tests for the update check API.
"""

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


class UpdateCheckTests(TestCase):
    """Test the update check API."""

    def test_update_check(self):
        client = APIClient()
        url = reverse('update-check')
        res = client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
