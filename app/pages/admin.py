from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from django_object_actions import DjangoObjectActions
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .admin_mixins import unfold_action
from .models import LandingPage
from .qr import generate_qr_png, generate_qr_svg


@admin.register(LandingPage)
class LandingPageAdmin(DjangoObjectActions, ModelAdmin):
    list_display = ["name", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "body"]
    readonly_fields = ["public_id", "created_at", "updated_at", "qr_preview"]

    fieldsets = [
        (None, {"fields": ["name", "body", "is_active"]}),
        (
            "QR Code Settings",
            {
                "fields": ["qr_error_correction", "qr_version", "qr_scale"],
                "classes": ["collapse"],
            },
        ),
        (
            "QR Code Preview",
            {
                "fields": ["qr_preview"],
            },
        ),
        (
            "Metadata",
            {
                "fields": ["public_id", "created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]

    change_actions = ["download_qr_code"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:pk>/qr/download/",
                self.admin_site.admin_view(self.qr_download),
                name="pages_landingpage_qr_download",
            ),
        ]
        return custom_urls + urls

    @admin.display(description="Preview")
    def qr_preview(self, obj):
        if not obj.pk:
            return "Save the page first to see QR code preview"
        preview_url = f"/p/{obj.public_id}/"
        svg = generate_qr_svg(
            preview_url,
            error=obj.qr_error_correction,
            version=obj.qr_version,
            scale=obj.qr_scale,
        )
        return format_html(
            '<div style="display: inline-block; background: white;">{}</div>', format_html(svg)
        )

    def qr_download(self, request, pk):
        obj = self.get_object(request, pk)
        full_url = request.build_absolute_uri(obj.get_absolute_url())
        png = generate_qr_png(
            full_url,
            error=obj.qr_error_correction,
            version=obj.qr_version,
            scale=obj.qr_scale,
        )
        response = HttpResponse(png, content_type="image/png")
        response["Content-Disposition"] = f'attachment; filename="{obj.public_id}.png"'
        return response

    @unfold_action(label="Download QR Code", short_description="Download QR as PNG")
    def download_qr_code(self, request, obj):
        url = reverse("admin:pages_landingpage_qr_download", args=[obj.pk])
        return HttpResponseRedirect(url)


# Unregister default admin classes to re-register with Unfold styling
admin.site.unregister(User)
admin.site.unregister(Group)

# Unregister unused admin views (OAuth and Site are configured via settings/env vars)
admin.site.unregister(Site)
admin.site.unregister(EmailAddress)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    """User admin with Unfold styling."""

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    """Group admin with Unfold styling."""

    pass
