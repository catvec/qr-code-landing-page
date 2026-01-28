import uuid

from django.db import models
from django.urls import reverse


class LandingPage(models.Model):
    """A landing page accessible via QR code."""

    class ErrorCorrection(models.TextChoices):
        LOW = 'L', 'Low (7%)'
        MEDIUM = 'M', 'Medium (15%)'
        QUARTILE = 'Q', 'Quartile (25%)'
        HIGH = 'H', 'High (30%)'

    # Public identifier - UUID4 for security
    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )

    # Content fields
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    # QR code settings
    qr_error_correction = models.CharField(
        max_length=1,
        choices=ErrorCorrection.choices,
        default=ErrorCorrection.HIGH,
        verbose_name='Error correction',
        help_text='Higher = more damage resistance but more modules',
    )
    qr_version = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Version',
        help_text='1-40. Leave blank for auto (minimum size)',
    )
    qr_scale = models.PositiveSmallIntegerField(
        default=10,
        verbose_name='Scale',
        help_text='Module size in pixels for PNG export',
    )
    qr_border = models.PositiveSmallIntegerField(
        default=4,
        verbose_name='Border',
        help_text='Quiet zone modules (spec requires 4)',
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:landing_page', kwargs={'public_id': self.public_id})
