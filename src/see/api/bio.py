"""API methods for Bio Page operations."""

from dataclasses import asdict

from ..models import (
    BioPageHistoryResponse,
    CreateBioPageRequest,
    CreateBioPageResponse,
    DeleteBioPageRequest,
    OperationResponse,
    UpdateBioPageRequest,
)
from .base import BaseAPI


class BioAPI(BaseAPI):
    """API methods for creating and managing bio pages."""

    async def create_bio_page(
        self, request: CreateBioPageRequest
    ) -> CreateBioPageResponse:
        response = await self._http_client.post("/v1/bio", json=asdict(request))
        return CreateBioPageResponse.from_dict(response)

    async def update_bio_page(self, request: UpdateBioPageRequest) -> OperationResponse:
        payload = asdict(request)
        if request.custom_links is None:
            payload.pop("custom_links")
        response = await self._http_client.put("/v1/bio", json=payload)
        return OperationResponse.from_dict(response)

    async def delete_bio_page(self, request: DeleteBioPageRequest) -> OperationResponse:
        response = await self._http_client.delete("/v1/bio", json=asdict(request))
        return OperationResponse.from_dict(response)

    async def get_bio_page_history(self, page: int = 1) -> BioPageHistoryResponse:
        response = await self._http_client.get("/v1/bios", params={"page": page})
        return BioPageHistoryResponse.from_dict(response)
