"""Data models for Bio Page operations."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class BioCustomLink:
    """A custom link displayed on a bio page."""

    title: str
    url: str
    description: str = ""


@dataclass(frozen=True)
class CreateBioPageRequest:
    """Request payload for creating a bio page."""

    title: str
    custom_links: list[BioCustomLink] = field(default_factory=list)
    custom_slug: str = ""
    description: str = ""
    domain: str = ""
    mastodon_url: str = ""
    rss_url: str = ""


@dataclass(frozen=True)
class UpdateBioPageRequest:
    """Request payload for updating a bio page."""

    id: int
    title: str
    custom_links: list[BioCustomLink] | None = None
    description: str = ""
    mastodon_url: str = ""
    rss_url: str = ""


@dataclass(frozen=True)
class DeleteBioPageRequest:
    """Request payload for deleting a bio page."""

    id: int


@dataclass(frozen=True)
class CreateBioPageResponse:
    """Response from creating a bio page."""

    code: int
    bio_page_id: int
    short_url: str
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CreateBioPageResponse":
        inner = data.get("data", {})
        return cls(
            code=data.get("code", 0),
            bio_page_id=inner.get("bio_page_id", 0),
            short_url=inner.get("short_url", ""),
            message=data.get("message", ""),
        )


@dataclass(frozen=True)
class BioPageHistoryItem:
    """One bio page history entry."""

    id: int = 0
    title: str = ""
    description: str = ""
    domain: str = ""
    slug: str = ""
    link: str = ""
    mastodon_url: str = ""
    rss_url: str = ""
    created_at: int = 0
    custom_links: list[dict[str, str]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BioPageHistoryItem":
        return cls(
            id=data.get("id", 0),
            title=data.get("title", ""),
            description=data.get("description", ""),
            domain=data.get("domain", ""),
            slug=data.get("slug", ""),
            link=data.get("link", ""),
            mastodon_url=data.get("mastodon_url", ""),
            rss_url=data.get("rss_url", ""),
            created_at=data.get("created_at", 0),
            custom_links=data.get("custom_links", []),
        )


@dataclass(frozen=True)
class BioPageHistoryResponse:
    """Paginated bio page history response."""

    code: int
    bio_pages: list[BioPageHistoryItem]
    total: int
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BioPageHistoryResponse":
        inner = data.get("data", {})
        return cls(
            code=data.get("code", 0),
            bio_pages=[
                BioPageHistoryItem.from_dict(item)
                for item in inner.get("bio_pages", [])
            ],
            total=inner.get("total", 0),
            message=data.get("message", ""),
        )
