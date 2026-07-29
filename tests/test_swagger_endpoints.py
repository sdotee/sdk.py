"""Contract tests for endpoints synchronized from the Swagger definition."""

import httpx
import pytest
from pytest_mock import MockerFixture

from see.client import SeeClient
from see.http_client import HttpClient
from see.models import (
    BioCustomLink,
    CreateBioPageRequest,
    CreateLargeFileUploadRequest,
    CreateQrcodeRequest,
    DeleteQrcodeRequest,
)


@pytest.mark.asyncio
async def test_bio_page_lifecycle(
    api_key: str, base_url: str, mocker: MockerFixture
) -> None:
    async with SeeClient(api_key=api_key, base_url=base_url) as client:
        mock_post = mocker.patch.object(
            client._http_client,
            "post",
            return_value={
                "code": 200,
                "data": {"bio_page_id": 7, "short_url": "https://s.ee/me"},
                "message": "ok",
            },
        )
        response = await client.create_bio_page(
            CreateBioPageRequest(
                title="Me",
                custom_links=[BioCustomLink(title="Site", url="https://example.com")],
            )
        )

        assert response.bio_page_id == 7
        mock_post.assert_called_once_with(
            "/v1/bio",
            json={
                "title": "Me",
                "custom_links": [
                    {"title": "Site", "url": "https://example.com", "description": ""}
                ],
                "custom_slug": "",
                "description": "",
                "domain": "",
                "mastodon_url": "",
                "rss_url": "",
            },
        )


@pytest.mark.asyncio
async def test_qrcode_and_history_endpoints(
    api_key: str, base_url: str, mocker: MockerFixture
) -> None:
    async with SeeClient(api_key=api_key, base_url=base_url) as client:
        mock_post = mocker.patch.object(
            client._http_client,
            "post",
            return_value={
                "code": 200,
                "data": {"slug": "qr", "png_url": "https://s.ee/qr.png"},
                "message": "ok",
            },
        )
        mock_delete = mocker.patch.object(
            client._http_client,
            "delete",
            return_value={"code": 200, "message": "deleted"},
        )
        mock_get = mocker.patch.object(
            client._http_client,
            "get",
            return_value={
                "code": 200,
                "data": {"qrcodes": [{"slug": "qr"}], "total": 1},
                "message": "ok",
            },
        )

        created = await client.create_qrcode(
            CreateQrcodeRequest(target_url="https://example.com", title="Example")
        )
        await client.delete_qrcode(DeleteQrcodeRequest(domain="s.ee", slug="qr"))
        history = await client.get_qrcode_history(page=2)

        assert created.data.png_url == "https://s.ee/qr.png"
        assert history.total == 1
        mock_post.assert_called_once()
        mock_delete.assert_called_once_with(
            "/v1/qrcode", json={"domain": "s.ee", "slug": "qr"}
        )
        mock_get.assert_called_once_with("/v1/qrcodes", params={"page": 2})


@pytest.mark.asyncio
async def test_account_and_history_endpoints(
    api_key: str, base_url: str, mocker: MockerFixture
) -> None:
    async with SeeClient(api_key=api_key, base_url=base_url) as client:
        mock_post = mocker.patch.object(
            client._http_client,
            "post",
            return_value={
                "code": 200,
                "data": {"token": "token", "expires_at": 100, "valid": True},
                "message": "ok",
            },
        )
        checked = await client.check_token("token")

        assert checked.valid is True
        mock_post.assert_called_once_with("/v1/token/check", json={"token": "token"})

        mock_get = mocker.patch.object(client._http_client, "get")
        mock_get.side_effect = [
            {"code": 200, "data": {"api_count_day": 3}, "message": "ok"},
            {"code": 200, "data": [{"slug": "a"}], "message": "ok"},
            {"code": 200, "data": [{"id": 1}], "message": "ok"},
            {"code": 200, "data": [{"file_id": 2}], "message": "ok"},
            {"code": 200, "data": {"visit_count": 9}, "message": "ok"},
        ]

        usage = await client.get_usage()
        links = await client.get_link_history(2)
        texts = await client.get_text_history(3)
        files = await client.get_file_history(4)
        stats = await client.get_link_visit_stat("s.ee", "a", "monthly")

        assert usage.data.api_count_day == 3
        assert links.data[0].slug == "a"
        assert texts.data[0].id == 1
        assert files.data[0].file_id == 2
        assert stats.visit_count == 9
        assert mock_get.call_args_list == [
            mocker.call("/v1/usage"),
            mocker.call("/v1/links", params={"page": 2}),
            mocker.call("/v1/texts", params={"page": 3}),
            mocker.call("/v1/files", params={"page": 4}),
            mocker.call(
                "/v1/link/visit-stat",
                params={"domain": "s.ee", "slug": "a", "period": "monthly"},
            ),
        ]


@pytest.mark.asyncio
async def test_simple_mode_shortening(
    api_key: str, base_url: str, mocker: MockerFixture
) -> None:
    async with SeeClient(api_key=api_key, base_url=base_url) as client:
        mock_get = mocker.patch.object(
            client._http_client,
            "get",
            return_value={"content": "https://s.ee/simple"},
        )

        result = await client.create_short_url_simple(
            "https://example.com", custom_slug="simple"
        )

        assert result == "https://s.ee/simple"
        mock_get.assert_called_once_with(
            "/v1/shorten",
            params={
                "signature": api_key,
                "url": "https://example.com",
                "custom_slug": "simple",
                "json": False,
            },
        )


@pytest.mark.asyncio
async def test_large_file_upload_lifecycle(
    api_key: str, base_url: str, mocker: MockerFixture
) -> None:
    async with SeeClient(api_key=api_key, base_url=base_url) as client:
        mock_post = mocker.patch.object(client._http_client, "post")
        mock_post.side_effect = [
            {
                "code": 200,
                "data": {"upload_id": "upload-1", "upload_url": "/tus/upload-1"},
                "message": "ok",
            },
            {
                "code": 200,
                "data": {"file": {"file_id": 8}, "short_link": "https://s.ee/f"},
                "message": "ok",
            },
        ]
        mock_patch = mocker.patch.object(client._http_client, "patch", return_value={})
        mock_head = mocker.patch.object(client._http_client, "head", return_value={})
        mock_delete = mocker.patch.object(
            client._http_client,
            "delete",
            return_value={"code": 200, "message": "cancelled"},
        )

        session = await client.create_large_file_upload(
            CreateLargeFileUploadRequest(file_name="video.mp4", file_size=4)
        )
        await client.upload_large_file_chunk("upload-1", b"data", 0)
        await client.check_large_file_upload("upload-1")
        await client.delete_large_file_tus_upload("upload-1")
        completed = await client.complete_large_file_upload("upload-1")
        await client.cancel_large_file_upload("upload-1")

        assert session.data.upload_id == "upload-1"
        assert completed.file is not None and completed.file.file_id == 8
        mock_patch.assert_called_once_with(
            "/v1/file/large-file-tus/upload-1",
            content=b"data",
            headers={
                "Content-Type": "application/offset+octet-stream",
                "Tus-Resumable": "1.0.0",
                "Upload-Offset": "0",
            },
        )
        mock_head.assert_called_once_with(
            "/v1/file/large-file-tus/upload-1",
            headers={"Tus-Resumable": "1.0.0"},
        )
        assert mock_delete.call_args_list == [
            mocker.call(
                "/v1/file/large-file-tus/upload-1",
                headers={"Tus-Resumable": "1.0.0"},
            ),
            mocker.call("/v1/file/large-file/cancel", json={"upload_id": "upload-1"}),
        ]


def test_http_client_accepts_no_content_response() -> None:
    client = HttpClient(api_key="token")
    response = httpx.Response(204, text="")

    assert client._handle_response(response) == {"content": ""}
