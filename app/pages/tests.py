import uuid

from django.test import Client, TestCase

from .models import LandingPage


class LandingPageViewTests(TestCase):
    """Tests for the public landing page view - the most critical feature."""

    def setUp(self):
        self.client = Client()

    def test_landing_page_returns_200_for_active_page(self):
        """Active landing pages should return 200."""
        page = LandingPage.objects.create(
            name="Test Page",
            body="Hello world",
            is_active=True,
        )
        response = self.client.get(f"/p/{page.public_id}/")
        self.assertEqual(response.status_code, 200)

    def test_landing_page_returns_404_for_inactive_page(self):
        """Inactive landing pages should return 404."""
        page = LandingPage.objects.create(
            name="Inactive Page",
            body="Should not be visible",
            is_active=False,
        )
        response = self.client.get(f"/p/{page.public_id}/")
        self.assertEqual(response.status_code, 404)

    def test_landing_page_returns_404_for_nonexistent_uuid(self):
        """Non-existent UUIDs should return 404, not 500."""
        fake_uuid = uuid.uuid4()
        response = self.client.get(f"/p/{fake_uuid}/")
        self.assertEqual(response.status_code, 404)

    def test_landing_page_renders_markdown_correctly(self):
        """Markdown content should be rendered to HTML."""
        page = LandingPage.objects.create(
            name="Markdown Test",
            body="# Hello\n\n**bold** text",
            is_active=True,
        )
        response = self.client.get(f"/p/{page.public_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Hello</h1>")
        self.assertContains(response, "<strong>bold</strong>")

    def test_landing_page_has_name_in_title(self):
        """Page name should appear in the page title."""
        page = LandingPage.objects.create(
            name="My Contact Info",
            body="Content here",
            is_active=True,
        )
        response = self.client.get(f"/p/{page.public_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Contact Info")

    def test_landing_page_handles_empty_body(self):
        """Empty body should not crash the page."""
        page = LandingPage.objects.create(
            name="Empty Page",
            body="",
            is_active=True,
        )
        response = self.client.get(f"/p/{page.public_id}/")
        self.assertEqual(response.status_code, 200)

    def test_landing_page_handles_special_characters(self):
        """Unicode, emoji, and special characters should work."""
        page = LandingPage.objects.create(
            name="Special Characters",
            body="Hello! Привет! こんにちは! 🧳✈️ <script>alert('xss')</script>",
            is_active=True,
        )
        response = self.client.get(f"/p/{page.public_id}/")
        self.assertEqual(response.status_code, 200)
        # Script tags should be escaped by markdown
        self.assertNotContains(response, "<script>alert")

    def test_landing_page_no_auth_required(self):
        """Landing pages should work without authentication."""
        page = LandingPage.objects.create(
            name="Public Page",
            body="Anyone can see this",
            is_active=True,
        )
        # Using a fresh client with no session
        client = Client()
        response = client.get(f"/p/{page.public_id}/")
        self.assertEqual(response.status_code, 200)


class LandingPageModelTests(TestCase):
    """Tests for the LandingPage model."""

    def test_public_id_is_auto_generated(self):
        """public_id should be automatically generated."""
        page = LandingPage.objects.create(name="Test", body="Content")
        self.assertIsNotNone(page.public_id)
        self.assertIsInstance(page.public_id, uuid.UUID)

    def test_public_id_is_unique(self):
        """Each page should have a unique public_id."""
        page1 = LandingPage.objects.create(name="Page 1", body="Content")
        page2 = LandingPage.objects.create(name="Page 2", body="Content")
        self.assertNotEqual(page1.public_id, page2.public_id)

    def test_default_qr_settings(self):
        """Default QR settings should be set correctly."""
        page = LandingPage.objects.create(name="Test", body="Content")
        self.assertEqual(page.qr_error_correction, "H")
        self.assertIsNone(page.qr_version)
        self.assertEqual(page.qr_scale, 10)

    def test_get_absolute_url(self):
        """get_absolute_url should return the correct path."""
        page = LandingPage.objects.create(name="Test", body="Content")
        url = page.get_absolute_url()
        self.assertEqual(url, f"/p/{page.public_id}/")
