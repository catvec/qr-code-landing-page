"""
Update the Django Site object to match the SITE_URL environment variable.

Required for django-allauth OAuth to generate correct callback URLs.

Usage:
    ./manage.py update_site_domain

Run after:
    - Initial migrations (creates Site table)
    - Changing SITE_URL environment variable
    - Deployment to sync Site with production URL
"""

from urllib.parse import urlparse

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Ensures the Site object matches the SITE_URL setting"

    def handle(self, *args, **options):
        # Get the site ID from settings (defaults to 1 if not set)
        site_id = getattr(settings, "SITE_ID", 1)

        # Get SITE_URL from settings
        site_url = settings.SITE_URL

        # Parse the domain from the SITE_URL
        parsed_url = urlparse(site_url)
        domain = parsed_url.netloc

        # Get or create the site object
        site = Site.objects.filter(pk=site_id).first()
        if site is None:
            raise ValueError(
                "Site not created yet (you probably need to run initial migrations)"
            )

        # Update the site if it already existed but domain differs
        if site.domain != domain or site.name != domain:
            old_domain = site.domain
            old_name = site.name

            site.domain = domain
            site.name = domain
            site.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully updated Site object (ID={site_id}): domain changed from "
                    f"'{old_domain}' to '{domain}', name changed from '{old_name}' to '{domain}'"
                )
            )
        else:
            self.stdout.write(
                f"Site object (ID={site_id}) already has the correct domain and name: '{domain}'"
            )
