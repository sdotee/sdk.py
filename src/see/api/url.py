from dataclasses import asdict

from ..exceptions import ValidationError
from ..models import (
    CreateShortUrlRequest,
    CreateShortUrlResponse,
    DeleteShortUrlRequest,
    DeleteShortUrlResponse,
    LinkHistoryResponse,
    LinkVisitStatResponse,
    UpdateShortUrlRequest,
    UpdateShortUrlResponse,
)
from .base import BaseAPI


class ShortUrlAPI(BaseAPI):
    """API methods for Short URL operations."""

    async def create_short_url_simple(
        self,
        url: str,
        *,
        domain: str | None = None,
        custom_slug: str | None = None,
        title: str | None = None,
        tag_ids: list[int] | None = None,
        password: str | None = None,
        expire_at: int | None = None,
        json_response: bool = False,
    ) -> CreateShortUrlResponse | str:
        """Create a short URL through the query-parameter based endpoint."""
        params = {
            key: value
            for key, value in {
                "signature": self._http_client.api_key,
                "url": url,
                "domain": domain,
                "custom_slug": custom_slug,
                "title": title,
                "tag_ids": tag_ids,
                "password": password,
                "expire_at": expire_at,
                "json": json_response,
            }.items()
            if value is not None
        }
        response = await self._http_client.get("/v1/shorten", params=params)
        if json_response:
            return CreateShortUrlResponse.from_dict(response)
        return str(response.get("content", response.get("data", "")))

    async def create_short_url(
        self, request: CreateShortUrlRequest
    ) -> CreateShortUrlResponse:
        """
        Create a new short URL.

        Args:
            request: The create short URL request containing domain, target URL, and optional parameters

        Returns:
            CreateShortUrlResponse: Response containing the created short URL details

        Raises:
            ValidationError: If target URL is invalid or domain is missing
            APIError: If the API request fails
        """
        # Validate target URL format
        if not request.target_url or not request.target_url.startswith(
            ("http://", "https://")
        ):
            raise ValidationError("Invalid URL: must start with http:// or https://")

        # Validate domain is provided
        if not request.domain:
            raise ValidationError("Domain is required")

        response = await self._http_client.post("/v1/shorten", json=asdict(request))
        return CreateShortUrlResponse.from_dict(response)

    async def update_short_url(
        self, request: UpdateShortUrlRequest
    ) -> UpdateShortUrlResponse:
        """
        Update an existing short URL.

        Args:
            request: The update short URL request containing domain, slug, and fields to update

        Returns:
            UpdateShortUrlResponse: Response indicating the update status

        Raises:
            NotFoundError: If the short URL is not found
            APIError: If the API request fails
        """
        response = await self._http_client.put(
            "/v1/shorten",
            json=asdict(request),
        )
        return UpdateShortUrlResponse.from_dict(response)

    async def delete_short_url(
        self, request: DeleteShortUrlRequest
    ) -> DeleteShortUrlResponse:
        """
        Delete a short URL.

        Args:
            request: The delete short URL request containing domain and slug

        Returns:
            DeleteShortUrlResponse: Response indicating the deletion status

        Raises:
            NotFoundError: If the short URL is not found
            APIError: If the API request fails
        """
        response = await self._http_client.delete("/v1/shorten", json=asdict(request))
        return DeleteShortUrlResponse.from_dict(response)

    async def get_link_history(self, page: int = 1) -> LinkHistoryResponse:
        """Get a page of short-link creation history."""
        response = await self._http_client.get("/v1/links", params={"page": page})
        return LinkHistoryResponse.from_dict(response)

    async def get_link_visit_stat(
        self,
        domain: str,
        slug: str,
        period: str = "totally",
    ) -> LinkVisitStatResponse:
        """Get visit statistics for a short link."""
        response = await self._http_client.get(
            "/v1/link/visit-stat",
            params={"domain": domain, "slug": slug, "period": period},
        )
        return LinkVisitStatResponse.from_dict(response)
