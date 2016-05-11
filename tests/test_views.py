from django.conf import settings

from django.core.urlresolvers import resolve, reverse
from django.test import TestCase, override_settings
from django.utils.baseconv import BaseConverter

from shortener.views import home_page

import pytest


@pytest.mark.django_db
@override_settings(CONVERTER=BaseConverter('01234'))
class ViewTests(TestCase):

    def test_home_page_view_found(self):
        """Test loading the home page."""
        found = resolve('/')
        self.assertEqual(found.func, home_page)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_first_redirect(self):
        """Test creating a redirect link."""
        token = settings.CONVERTER.encode(1)
        full_url = 'http://www.google.com'

        expected_redirect_url = reverse('preview', args=token)
        response = self.client.post('/', {'url': full_url})
        self.assertRedirects(response, expected_redirect_url)

        response = self.client.get(expected_redirect_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['full_url'], full_url)

        # verify the URL is also actually included in the rendered output, both
        # as the readable text and as the anchor around it.
        self.assertContains(response, full_url, 2)

    def test_get_nonexistent_preview(self):
        """Test 404 handling of nonexistent tokens."""
        token = 'bogustoken!'
        url = reverse(
            'token_redirect',
            kwargs={'token': token}
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
