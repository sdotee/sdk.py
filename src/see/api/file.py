from dataclasses import asdict
from pathlib import Path

from ..models import (
    CompleteLargeFileUploadResponse,
    CreateLargeFileUploadRequest,
    CreateLargeFileUploadResponse,
    DeleteFileResponse,
    DomainResponse,
    FileHistoryResponse,
    LargeFileUploadProgressResponse,
    OperationResponse,
    PrivateFileUrlResponse,
    UploadFileResponse,
)
from .base import BaseAPI


class FileAPI(BaseAPI):
    """API methods for File Sharing operations."""

    async def upload_file(
        self,
        file_path: str,
        domain: str | None = None,
        custom_slug: str | None = None,
    ) -> UploadFileResponse:
        """
        Upload a file.

        Args:
            file_path: Path to the file to upload
            domain: Optional domain for the short link
            custom_slug: Optional custom slug for the short link

        Returns:
            UploadFileResponse: Response containing the uploaded file details

        Raises:
            APIError: If the API request fails
            IOError: If the file cannot be read
        """
        path = Path(file_path)
        filename = path.name
        form_data = {
            key: value
            for key, value in {"domain": domain, "custom_slug": custom_slug}.items()
            if value is not None
        }

        with path.open("rb") as f:
            # httpx will handle the multipart encoding by providing `files`.
            files = {"file": (filename, f)}

            response = await self._http_client.post(
                "/v1/file/upload",
                files=files,
                data=form_data,
            )
            return UploadFileResponse.from_dict(response)

    async def delete_file(self, hash_str: str) -> DeleteFileResponse:
        """
        Delete a file.

        Args:
            hash_str: The hash of the file to delete

        Returns:
            DeleteFileResponse: Response indicating the deletion status

        Raises:
            APIError: If the API request fails
        """
        # The doc says /delete/string, likely /delete/{hash}
        response = await self._http_client.get(f"/v1/file/delete/{hash_str}")
        return DeleteFileResponse.from_dict(response)

    async def get_file_domains(self) -> DomainResponse:
        """
        Get available domains for file sharing.

        Returns:
            DomainResponse: Response containing the list of available domains

        Raises:
            APIError: If the API request fails
        """
        response = await self._http_client.get("/v1/file/domains")
        return DomainResponse.from_dict(response)

    async def get_file_history(self, page: int = 1) -> FileHistoryResponse:
        """Get a page of uploaded file history."""
        response = await self._http_client.get("/v1/files", params={"page": page})
        return FileHistoryResponse.from_dict(response)

    async def get_private_file_download_url(
        self, file_id: int
    ) -> PrivateFileUrlResponse:
        """Get a temporary download URL for a private file."""
        response = await self._http_client.get(
            "/v1/file/private/download-url", params={"file_id": file_id}
        )
        return PrivateFileUrlResponse.from_dict(response)

    async def create_large_file_upload(
        self, request: CreateLargeFileUploadRequest
    ) -> CreateLargeFileUploadResponse:
        """Create a resumable large-file upload session."""
        response = await self._http_client.post(
            "/v1/file/large-file/create", json=asdict(request)
        )
        return CreateLargeFileUploadResponse.from_dict(response)

    async def upload_large_file_chunk(
        self, upload_id: str, chunk: bytes, offset: int
    ) -> None:
        """Upload one TUS chunk at the given byte offset."""
        await self._http_client.patch(
            f"/v1/file/large-file-tus/{upload_id}",
            content=chunk,
            headers={
                "Content-Type": "application/offset+octet-stream",
                "Tus-Resumable": "1.0.0",
                "Upload-Offset": str(offset),
            },
        )

    async def check_large_file_upload(self, upload_id: str) -> None:
        """Send a TUS HEAD request to validate an upload session."""
        await self._http_client.head(
            f"/v1/file/large-file-tus/{upload_id}",
            headers={"Tus-Resumable": "1.0.0"},
        )

    async def delete_large_file_tus_upload(self, upload_id: str) -> None:
        """Terminate a resumable upload through its TUS endpoint."""
        await self._http_client.delete(
            f"/v1/file/large-file-tus/{upload_id}",
            headers={"Tus-Resumable": "1.0.0"},
        )

    async def get_large_file_upload_progress(
        self, upload_id: str
    ) -> LargeFileUploadProgressResponse:
        """Get the server-side progress of a large-file upload."""
        response = await self._http_client.get(
            "/v1/file/large-file/progress", params={"upload_id": upload_id}
        )
        return LargeFileUploadProgressResponse.from_dict(response)

    async def complete_large_file_upload(
        self, upload_id: str
    ) -> CompleteLargeFileUploadResponse:
        """Finalize a fully uploaded large file."""
        response = await self._http_client.post(
            "/v1/file/large-file/complete", json={"upload_id": upload_id}
        )
        return CompleteLargeFileUploadResponse.from_dict(response)

    async def cancel_large_file_upload(self, upload_id: str) -> OperationResponse:
        """Cancel a large-file upload and remove temporary data."""
        response = await self._http_client.delete(
            "/v1/file/large-file/cancel", json={"upload_id": upload_id}
        )
        return OperationResponse.from_dict(response)
