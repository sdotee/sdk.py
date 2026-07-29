"""Data models for Text Sharing operations."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CreateTextRequest:
    """Represents a request payload to create a text sharing."""

    content: str
    title: str
    custom_slug: str = ""
    domain: str = "fs.to"
    expire_at: int = 0
    password: str = ""
    tag_ids: list[int] = field(default_factory=list)
    text_type: str = "plain_text"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CreateTextRequest":
        return cls(
            content=data.get("content", ""),
            title=data.get("title", ""),
            custom_slug=data.get("custom_slug", ""),
            domain=data.get("domain", "fs.to"),
            expire_at=data.get("expire_at", 0),
            password=data.get("password", ""),
            tag_ids=data.get("tag_ids", []),
            text_type=data.get("text_type", "plain_text"),
        )


@dataclass(frozen=True)
class TextHistoryItem:
    """Represents one text sharing history entry."""

    id: int = 0
    title: str = ""
    domain: str = ""
    slug: str = ""
    short_url: str = ""
    content_preview: str = ""
    text_type: str = ""
    created_at: int = 0
    is_expired: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TextHistoryItem":
        return cls(
            **{
                key: data.get(key, default)
                for key, default in {
                    "id": 0,
                    "title": "",
                    "domain": "",
                    "slug": "",
                    "short_url": "",
                    "content_preview": "",
                    "text_type": "",
                    "created_at": 0,
                    "is_expired": False,
                }.items()
            }
        )


@dataclass(frozen=True)
class TextHistoryResponse:
    """Represents a paginated text sharing history response."""

    code: int
    data: list[TextHistoryItem]
    message: str
    success: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TextHistoryResponse":
        return cls(
            code=data.get("code", 0),
            data=[TextHistoryItem.from_dict(item) for item in data.get("data", [])],
            message=data.get("message", ""),
            success=data.get("success", False),
        )


@dataclass(frozen=True)
class CreateTextResponse:
    """Represents a response payload from creating a text sharing."""

    code: int
    custom_slug: str
    short_url: str
    slug: str
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CreateTextResponse":
        inner_data = data.get("data", {})
        return cls(
            code=data.get("code", 0),
            custom_slug=inner_data.get("custom_slug", ""),
            short_url=inner_data.get("short_url", ""),
            slug=inner_data.get("slug", ""),
            message=data.get("message", ""),
        )


@dataclass(frozen=True)
class UpdateTextRequest:
    """Represents a request payload to update a text sharing."""

    content: str
    domain: str
    slug: str
    title: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UpdateTextRequest":
        return cls(
            content=data.get("content", ""),
            domain=data.get("domain", ""),
            slug=data.get("slug", ""),
            title=data.get("title", ""),
        )


@dataclass(frozen=True)
class UpdateTextResponse:
    """Represents a response payload from updating a text sharing."""

    code: int
    message: str
    data: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UpdateTextResponse":
        return cls(
            code=data.get("code", 0),
            message=data.get("message", ""),
            data=data.get("data", {}),
        )


@dataclass(frozen=True)
class DeleteTextRequest:
    """Represents a request payload to delete a text sharing."""

    domain: str
    slug: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DeleteTextRequest":
        return cls(
            domain=data.get("domain", ""),
            slug=data.get("slug", ""),
        )


@dataclass(frozen=True)
class DeleteTextResponse:
    """Represents a response payload from deleting a text sharing."""

    code: int
    message: str
    data: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DeleteTextResponse":
        return cls(
            code=data.get("code", 0),
            message=data.get("message", ""),
            data=data.get("data", {}),
        )
