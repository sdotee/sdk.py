"""Data models for QR Code operations."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CreateQrcodeRequest:
    """Request payload for creating a dynamic QR code."""

    target_url: str
    title: str
    custom_slug: str = ""
    domain: str = ""


@dataclass(frozen=True)
class DeleteQrcodeRequest:
    """Request payload for deleting a QR code."""

    domain: str
    slug: str


@dataclass(frozen=True)
class QrcodeItem:
    """QR code details returned by create and history endpoints."""

    title: str = ""
    domain: str = ""
    custom_slug: str = ""
    slug: str = ""
    short_url: str = ""
    png_url: str = ""
    svg_url: str = ""
    pdf_url: str = ""
    created_at: int = 0
    scan_count: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QrcodeItem":
        return cls(
            title=data.get("title", ""),
            domain=data.get("domain", ""),
            custom_slug=data.get("custom_slug", ""),
            slug=data.get("slug", ""),
            short_url=data.get("short_url", ""),
            png_url=data.get("png_url", ""),
            svg_url=data.get("svg_url", ""),
            pdf_url=data.get("pdf_url", ""),
            created_at=data.get("created_at", 0),
            scan_count=data.get("scan_count", 0),
        )


@dataclass(frozen=True)
class CreateQrcodeResponse:
    """Response from creating a QR code."""

    code: int
    data: QrcodeItem
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CreateQrcodeResponse":
        return cls(
            code=data.get("code", 0),
            data=QrcodeItem.from_dict(data.get("data", {})),
            message=data.get("message", ""),
        )


@dataclass(frozen=True)
class QrcodeHistoryResponse:
    """Paginated QR code history response."""

    code: int
    qrcodes: list[QrcodeItem]
    total: int
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QrcodeHistoryResponse":
        inner = data.get("data", {})
        return cls(
            code=data.get("code", 0),
            qrcodes=[QrcodeItem.from_dict(item) for item in inner.get("qrcodes", [])],
            total=inner.get("total", 0),
            message=data.get("message", ""),
        )
