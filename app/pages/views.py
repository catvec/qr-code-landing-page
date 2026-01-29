import bleach
import markdown
from django.shortcuts import get_object_or_404, render

from .models import LandingPage

ALLOWED_TAGS = [
    "h1", "h2", "h3", "h4", "h5", "h6",
    "p", "br", "hr",
    "strong", "em", "b", "i", "u", "s", "del", "ins",
    "a", "code", "pre", "blockquote",
    "ul", "ol", "li",
    "table", "thead", "tbody", "tr", "th", "td",
    "img",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
    "img": ["src", "alt", "title"],
    "th": ["align"],
    "td": ["align"],
}


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

    # Sanitize HTML to prevent XSS
    html_content = bleach.clean(
        html_content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
    )

    return render(
        request,
        "pages/landing_page.html",
        {
            "page": page,
            "content": html_content,
        },
    )
