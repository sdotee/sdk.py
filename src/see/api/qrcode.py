"""API methods for QR Code operations."""

from dataclasses import asdict

from ..models import (
    CreateQrcodeRequest,
    CreateQrcodeResponse,
    DeleteQrcodeRequest,
    OperationResponse,
    QrcodeHistoryResponse,
)
from .base import BaseAPI


class QrcodeAPI(BaseAPI):
    """API methods for creating and managing dynamic QR codes."""

    async def create_qrcode(self, request: CreateQrcodeRequest) -> CreateQrcodeResponse:
        response = await self._http_client.post("/v1/qrcode", json=asdict(request))
        return CreateQrcodeResponse.from_dict(response)

    async def delete_qrcode(self, request: DeleteQrcodeRequest) -> OperationResponse:
        response = await self._http_client.delete("/v1/qrcode", json=asdict(request))
        return OperationResponse.from_dict(response)

    async def get_qrcode_history(self, page: int = 1) -> QrcodeHistoryResponse:
        response = await self._http_client.get("/v1/qrcodes", params={"page": page})
        return QrcodeHistoryResponse.from_dict(response)
