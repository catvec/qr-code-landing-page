import markdown
from django.shortcuts import get_object_or_404, render

from .models import LandingPage


def landing_page(request, public_id):
    """Display a landing page with rendered markdown content."""
    page = get_object_or_404(LandingPage, public_id=public_id, is_active=True)

    html_content = markdown.markdown(
        page.body,
        extensions=[
            "markdown.extensions.fenced_code",
            "markdown.extensions.tables",
            "markdown.extensions.nl2br",
        ],
    )

    return render(
        request,
        "pages/landing_page.html",
        {
            "page": page,
            "content": html_content,
        },
    )
