import io

import segno


def generate_qr_svg(url: str, error: str = 'H', version: int | None = None,
                    scale: int = 4, border: int = 4) -> str:
    """Generate QR code as SVG string."""
    qr = segno.make(url, error=error, version=version)
    buffer = io.StringIO()
    qr.save(buffer, kind='svg', scale=scale, border=border)
    return buffer.getvalue()


def generate_qr_png(url: str, error: str = 'H', version: int | None = None,
                    scale: int = 10, border: int = 4) -> bytes:
    """Generate QR code as PNG bytes."""
    qr = segno.make(url, error=error, version=version)
    buffer = io.BytesIO()
    qr.save(buffer, kind='png', scale=scale, border=border)
    return buffer.getvalue()
