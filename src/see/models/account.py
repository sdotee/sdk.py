"""Data models for token and account usage operations."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TokenCheckResponse:
    """Response from validating an API token."""

    code: int
    token: str
    expires_at: int
    valid: bool
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TokenCheckResponse":
        inner = data.get("data", {})
        return cls(
            code=data.get("code", 0),
            token=inner.get("token", ""),
            expires_at=inner.get("expires_at", 0),
            valid=inner.get("valid", False),
            message=data.get("message", ""),
        )


@dataclass(frozen=True)
class Usage:
    """Account usage counters and limits."""

    api_count_day: int = 0
    api_count_day_limit: int = 0
    api_count_month: int = 0
    api_count_month_limit: int = 0
    file_count: int = 0
    link_count_day: int = 0
    link_count_day_limit: int = 0
    link_count_month: int = 0
    link_count_month_limit: int = 0
    qrcode_count_day: int = 0
    qrcode_count_day_limit: int = 0
    qrcode_count_month: int = 0
    qrcode_count_month_limit: int = 0
    storage_usage_limit_mb: str = ""
    storage_usage_mb: str = ""
    text_count_day: int = 0
    text_count_day_limit: int = 0
    text_count_month: int = 0
    text_count_month_limit: int = 0
    upload_count_day: int = 0
    upload_count_day_limit: int = 0
    upload_count_month: int = 0
    upload_count_month_limit: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Usage":
        fields = cls.__dataclass_fields__
        return cls(
            **{name: data.get(name, field.default) for name, field in fields.items()}
        )


@dataclass(frozen=True)
class UsageResponse:
    """Response containing account usage counters."""

    code: int
    data: Usage
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UsageResponse":
        return cls(
            code=data.get("code", 0),
            data=Usage.from_dict(data.get("data", {})),
            message=data.get("message", ""),
        )
