"""API methods for token and account operations."""

from ..models import TokenCheckResponse, UsageResponse
from .base import BaseAPI


class AccountAPI(BaseAPI):
    """API methods for token validation and usage reporting."""

    async def check_token(self, token: str) -> TokenCheckResponse:
        response = await self._http_client.post(
            "/v1/token/check", json={"token": token}
        )
        return TokenCheckResponse.from_dict(response)

    async def get_usage(self) -> UsageResponse:
        response = await self._http_client.get("/v1/usage")
        return UsageResponse.from_dict(response)
