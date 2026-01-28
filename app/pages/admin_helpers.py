"""Helper utilities for custom admin views."""

from django.contrib import admin
from django.shortcuts import render


def admin_render(request, template_name, context=None):
    """
    Render a template with admin site context automatically included.

    This ensures custom admin pages have access to the sidebar, branding,
    and other admin UI elements.
    """
    if context is None:
        context = {}

    full_context = {
        **admin.site.each_context(request),
        **context,
    }

    return render(request, template_name, full_context)
