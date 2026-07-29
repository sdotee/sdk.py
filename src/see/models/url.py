"""Data models for Short URL operations."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CreateShortUrlRequest:
    """Represents a request payload to create/shorten a URL."""

    domain: str
    target_url: str
    expiration_redirect_url: str = ""
    expire_at: int = 0  # Unix timestamp (seconds) or None
    password: str = ""
    title: str = ""
    custom_slug: str = ""
    tag_ids: list[int] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CreateShortUrlRequest":
        """Create a CreateShortUrlRequest instance from a dictionary."""
        return cls(
            domain=data.get("domain", ""),
            target_url=data.get("target_url", ""),
            custom_slug=data.get("custom_slug", ""),
            expiration_redirect_url=data.get("expiration_redirect_url", ""),
            expire_at=data.get("expire_at", 0),
            password=data.get("password", ""),
            tag_ids=data.get("tag_ids", []),
            title=data.get("title", ""),
        )


@dataclass(frozen=True)
class CreateShortUrlResponse:
    """Represents a response payload from creating a shortened URL."""

    code: int
    data: dict[str, Any]
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CreateShortUrlResponse":
        """Create a CreateShortUrlResponse instance from a dictionary."""
        return cls(
            code=data.get("code", 0),
            data=data.get("data", {}),
            message=data.get("message", ""),
        )


@dataclass(frozen=True)
class UpdateShortUrlRequest:
    """Represents a request payload to update a shortened URL."""

    domain: str
    slug: str
    target_url: str
    title: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UpdateShortUrlRequest":
        """Create an UpdateShortUrlRequest instance from a dictionary."""
        return cls(
            domain=data.get("domain", ""),
            slug=data.get("slug", ""),
            target_url=data.get("target_url", ""),
            title=data.get("title", ""),
        )


@dataclass(frozen=True)
class UpdateShortUrlResponse:
    """Represents a response payload from updating a shortened URL."""

    code: int
    data: str = ""
    message: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UpdateShortUrlResponse":
        """Create an UpdateShortUrlResponse instance from a dictionary."""
        return cls(
            code=data.get("code", 0),
            data=data.get("data", ""),
            message=data.get("message", ""),
        )


@dataclass(frozen=True)
class DeleteShortUrlRequest:
    """Represents a request payload to delete a shortened URL."""

    domain: str
    slug: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DeleteShortUrlRequest":
        """Create a DeleteShortUrlRequest instance from a dictionary."""
        return cls(
            domain=data.get("domain", ""),
            slug=data.get("slug", ""),
        )


@dataclass(frozen=True)
class DeleteShortUrlResponse:
    """Represents a response payload from deleting a shortened URL."""

    code: int
    data: str = ""
    message: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DeleteShortUrlResponse":
        """Create a DeleteShortUrlResponse instance from a dictionary."""
        return cls(
            code=data.get("code", 0),
            data=data.get("data", ""),
            message=data.get("message", ""),
        )


@dataclass(frozen=True)
class LinkHistoryItem:
    """Represents one short-link history entry."""

    created_at: int = 0
    domain: str = ""
    object_type: int = 0
    short_url: str = ""
    slug: str = ""
    target_url: str = ""
    title: str = ""
    visit_count: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LinkHistoryItem":
        return cls(
            **{
                key: data.get(key, default)
                for key, default in {
                    "created_at": 0,
                    "domain": "",
                    "object_type": 0,
                    "short_url": "",
                    "slug": "",
                    "target_url": "",
                    "title": "",
                    "visit_count": 0,
                }.items()
            }
        )


@dataclass(frozen=True)
class LinkHistoryResponse:
    """Represents a paginated short-link history response."""

    code: int
    data: list[LinkHistoryItem]
    message: str
    success: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LinkHistoryResponse":
        return cls(
            code=data.get("code", 0),
            data=[LinkHistoryItem.from_dict(item) for item in data.get("data", [])],
            message=data.get("message", ""),
            success=data.get("success", False),
        )


@dataclass(frozen=True)
class LinkVisitStatResponse:
    """Represents visit statistics for a short link."""

    code: int
    visit_count: int
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LinkVisitStatResponse":
        return cls(
            code=data.get("code", 0),
            visit_count=data.get("data", {}).get("visit_count", 0),
            message=data.get("message", ""),
        )
