from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse
from django.utils.html import format_html
from django_object_actions import DjangoObjectActions
from unfold.admin import ModelAdmin

from .admin_mixins import unfold_action
from .models import LandingPage
from .qr import generate_qr_png, generate_qr_svg


@admin.register(LandingPage)
class LandingPageAdmin(DjangoObjectActions, ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'body']
    readonly_fields = ['public_id', 'created_at', 'updated_at', 'qr_preview']

    fieldsets = [
        (None, {
            'fields': ['title', 'body', 'is_active']
        }),
        ('QR Code Settings', {
            'fields': ['qr_error_correction', 'qr_version', 'qr_scale', 'qr_border'],
            'classes': ['collapse'],
        }),
        ('QR Code Preview', {
            'fields': ['qr_preview'],
        }),
        ('Metadata', {
            'fields': ['public_id', 'created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]

    change_actions = ['view_page', 'view_qr_code', 'download_qr_code']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:pk>/qr/',
                self.admin_site.admin_view(self.qr_view),
                name='pages_landingpage_qr',
            ),
            path(
                '<int:pk>/qr/download/',
                self.admin_site.admin_view(self.qr_download),
                name='pages_landingpage_qr_download',
            ),
        ]
        return custom_urls + urls

    def qr_preview(self, obj):
        if not obj.pk:
            return "Save the page first to see QR code preview"
        preview_url = f"/p/{obj.public_id}/"
        svg = generate_qr_svg(
            preview_url,
            error=obj.qr_error_correction,
            version=obj.qr_version,
            scale=4,
            border=obj.qr_border,
        )
        return format_html('<div style="max-width: 200px;">{}</div>', format_html(svg))
    qr_preview.short_description = 'Preview'

    def qr_view(self, request, pk):
        obj = self.get_object(request, pk)
        full_url = request.build_absolute_uri(obj.get_absolute_url())
        svg = generate_qr_svg(
            full_url,
            error=obj.qr_error_correction,
            version=obj.qr_version,
            scale=6,
            border=obj.qr_border,
        )
        return render(request, 'pages/qr_view.html', {
            'page': obj,
            'qr_svg': svg,
            'full_url': full_url,
            'download_url': reverse('admin:pages_landingpage_qr_download', args=[obj.pk]),
        })

    def qr_download(self, request, pk):
        obj = self.get_object(request, pk)
        full_url = request.build_absolute_uri(obj.get_absolute_url())
        png = generate_qr_png(
            full_url,
            error=obj.qr_error_correction,
            version=obj.qr_version,
            scale=obj.qr_scale,
            border=obj.qr_border,
        )
        response = HttpResponse(png, content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{obj.public_id}.png"'
        return response

    @unfold_action(label="View Page", short_description="Open landing page")
    def view_page(self, request, obj):
        return HttpResponseRedirect(obj.get_absolute_url())

    @unfold_action(label="View QR Code", short_description="View QR code")
    def view_qr_code(self, request, obj):
        url = reverse('admin:pages_landingpage_qr', args=[obj.pk])
        return HttpResponseRedirect(url)

    @unfold_action(label="Download QR Code", short_description="Download QR as PNG")
    def download_qr_code(self, request, obj):
        url = reverse('admin:pages_landingpage_qr_download', args=[obj.pk])
        return HttpResponseRedirect(url)
