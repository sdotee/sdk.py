"""Data models for File Sharing operations."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class UploadFileResponse:
    """Represents a response payload from uploading a file."""

    code: int
    file_id: int
    filename: str
    hash: str
    url: str
    message: str
    delete_url: str = ""
    page_url: str = ""
    width: int = 0
    height: int = 0
    size: int = 0
    storename: str = ""
    path: str = ""
    mime_type: str = ""
    thumb_url: str = ""
    upload_status: int = 0
    created_at: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UploadFileResponse":
        inner = data.get("data", {})
        return cls(
            code=data.get("code", 0),
            message=data.get("message", ""),
            file_id=inner.get("file_id", 0),
            filename=inner.get("filename", ""),
            hash=inner.get("hash", ""),
            url=inner.get("url", ""),
            delete_url=inner.get("delete", ""),
            page_url=inner.get("page", ""),
            width=inner.get("width", 0),
            height=inner.get("height", 0),
            size=inner.get("size", 0),
            storename=inner.get("storename", ""),
            path=inner.get("path", ""),
            mime_type=inner.get("mime_type", ""),
            thumb_url=inner.get("thumb_url", ""),
            upload_status=inner.get("upload_status", 0),
            created_at=inner.get("created_at", 0),
        )


@dataclass(frozen=True)
class DeleteFileResponse:
    """Represents a response payload from deleting a file."""

    code: str
    message: str
    success: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DeleteFileResponse":
        return cls(
            code=str(data.get("code", "")),
            message=data.get("message", ""),
            success=data.get("success", False),
        )


@dataclass(frozen=True)
class FileItem:
    """File details returned by file history and large upload endpoints."""

    file_id: int = 0
    filename: str = ""
    hash: str = ""
    url: str = ""
    delete_url: str = ""
    page_url: str = ""
    width: int = 0
    height: int = 0
    size: int = 0
    storename: str = ""
    path: str = ""
    mime_type: str = ""
    thumb_url: str = ""
    upload_status: int = 0
    created_at: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FileItem":
        return cls(
            file_id=data.get("file_id", 0),
            filename=data.get("filename", ""),
            hash=data.get("hash", ""),
            url=data.get("url", ""),
            delete_url=data.get("delete", ""),
            page_url=data.get("page", ""),
            width=data.get("width", 0),
            height=data.get("height", 0),
            size=data.get("size", 0),
            storename=data.get("storename", ""),
            path=data.get("path", ""),
            mime_type=data.get("mime_type", ""),
            thumb_url=data.get("thumb_url", ""),
            upload_status=data.get("upload_status", 0),
            created_at=data.get("created_at", 0),
        )


@dataclass(frozen=True)
class FileHistoryResponse:
    """Paginated file upload history response."""

    code: int
    data: list[FileItem]
    message: str
    success: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FileHistoryResponse":
        return cls(
            code=data.get("code", 0),
            data=[FileItem.from_dict(item) for item in data.get("data", [])],
            message=data.get("message", ""),
            success=data.get("success", False),
        )


@dataclass(frozen=True)
class PrivateFileUrlResponse:
    """Response containing a temporary private-file download URL."""

    code: int
    file_id: int
    url: str
    expires_at: int
    message: str
    success: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PrivateFileUrlResponse":
        inner = data.get("data", {})
        return cls(
            code=data.get("code", 0),
            file_id=inner.get("file_id", 0),
            url=inner.get("url", ""),
            expires_at=inner.get("expires_at", 0),
            message=data.get("message", ""),
            success=data.get("success", False),
        )


@dataclass(frozen=True)
class CreateLargeFileUploadRequest:
    """Request payload for creating a resumable large-file upload."""

    file_name: str
    file_size: int
    alias: str = ""
    description: str = ""
    domain: str = ""
    expire_at: int = 0
    file_hash: str = ""
    is_private: int = 0
    mime_type: str = ""
    password: str = ""
    title: str = ""


@dataclass(frozen=True)
class LargeFileUploadSession:
    """A resumable large-file upload session."""

    id: int = 0
    upload_id: str = ""
    upload_url: str = ""
    file_size: int = 0
    expires_at: int = 0
    fast_upload: bool = False
    existing_file: FileItem | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LargeFileUploadSession":
        existing = data.get("existing_file")
        return cls(
            id=data.get("id", 0),
            upload_id=data.get("upload_id", ""),
            upload_url=data.get("upload_url", ""),
            file_size=data.get("file_size", 0),
            expires_at=data.get("expires_at", 0),
            fast_upload=data.get("fast_upload", False),
            existing_file=FileItem.from_dict(existing) if existing else None,
        )


@dataclass(frozen=True)
class CreateLargeFileUploadResponse:
    """Response from creating a large-file upload session."""

    code: int
    data: LargeFileUploadSession
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CreateLargeFileUploadResponse":
        return cls(
            code=data.get("code", 0),
            data=LargeFileUploadSession.from_dict(data.get("data", {})),
            message=data.get("message", ""),
        )


@dataclass(frozen=True)
class LargeFileUploadProgress:
    """Current progress of a resumable upload."""

    upload_id: str = ""
    file_name: str = ""
    file_size: int = 0
    uploaded_size: int = 0
    progress: float = 0.0
    status: int = 0
    created_at: int = 0
    updated_at: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LargeFileUploadProgress":
        fields = cls.__dataclass_fields__
        return cls(
            **{name: data.get(name, field.default) for name, field in fields.items()}
        )


@dataclass(frozen=True)
class LargeFileUploadProgressResponse:
    """Response containing resumable upload progress."""

    code: int
    data: LargeFileUploadProgress
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LargeFileUploadProgressResponse":
        return cls(
            code=data.get("code", 0),
            data=LargeFileUploadProgress.from_dict(data.get("data", {})),
            message=data.get("message", ""),
        )


@dataclass(frozen=True)
class CompleteLargeFileUploadResponse:
    """Response from completing a resumable upload."""

    code: int
    file: FileItem | None
    short_link: str
    message: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CompleteLargeFileUploadResponse":
        inner = data.get("data", {})
        file_data = inner.get("file")
        return cls(
            code=data.get("code", 0),
            file=FileItem.from_dict(file_data) if file_data else None,
            short_link=inner.get("short_link", ""),
            message=data.get("message", ""),
        )
