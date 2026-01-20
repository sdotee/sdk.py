"""
Complete example demonstrating all features of the SEE URL SDK.

This example shows comprehensive usage of the SDK including:
- Creating short URLs with various options
- Updating and deleting short URLs
- Getting available domains and tags
- Error handling
- Batch operations

Make sure to set your API key as an environment variable before running:
    export SEE_API_KEY="your-api-key-here"
"""

import asyncio
import os
from datetime import datetime, timedelta

from see import SeeClient
from see.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
)
from see.models import (
    CreateShortUrlRequest,
    DeleteShortUrlRequest,
    UpdateShortUrlRequest,
)


async def basic_usage_example(api_key: str) -> None:
    """Demonstrate basic usage of the SDK."""
    print("=== Basic Usage Example ===")
    print()

    async with SeeClient(api_key=api_key) as client:
        # Create a basic short URL request
        request = CreateShortUrlRequest(
            domain="s.ee",
            target_url="https://example.com/very/long/url/to/shorten",
            title="Example URL",
        )

        # Create the short URL
        response = await client.create_short_url(request)

        print(f"Response code: {response.code}")
        print(f"Message: {response.message}")
        print(f"Data: {response.data}")
        print()


async def custom_short_url_example(api_key: str) -> None:
    """Demonstrate creating a custom short URL with advanced options."""
    print("=== Custom Short URL Example ===")
    print()

    async with SeeClient(api_key=api_key) as client:
        # Calculate expiration time (30 days from now)
        expire_timestamp = int((datetime.now() + timedelta(days=30)).timestamp())

        # Create with custom slug and advanced options
        request = CreateShortUrlRequest(
            domain="s.ee",
            target_url="https://example.com/product/special-offer",
            custom_slug="summer2025",  # Custom short code
            title="Summer 2025 Special Offer",
            expire_at=expire_timestamp,  # Unix timestamp
            expiration_redirect_url="https://example.com/offers",  # Redirect after expiration
            password="optional-password",  # Optional password protection
            tag_ids=[1, 2],  # Optional tag IDs for categorization
        )

        response = await client.create_short_url(request)

        print(f"Response code: {response.code}")
        print(f"Message: {response.message}")
        print(f"Custom URL data: {response.data}")
        print(f"Expires at: {datetime.fromtimestamp(expire_timestamp)}")
        print()


async def manage_urls_example(api_key: str) -> None:
    """Demonstrate updating and deleting short URLs."""
    print("=== Manage URLs Example ===")
    print()

    async with SeeClient(api_key=api_key) as client:
        # First, create a short URL to manage
        create_request = CreateShortUrlRequest(
            domain="s.ee",
            target_url="https://example.com/page-to-update",
            custom_slug="example-update",
            title="Original Title",
        )

        create_response = await client.create_short_url(create_request)
        print(f"Created URL: {create_response.data}")
        print()

        # Update the short URL
        update_request = UpdateShortUrlRequest(
            domain="s.ee",
            slug="example-update",
            target_url="https://example.com/updated-page",
            title="Updated Title",
        )

        update_response = await client.update_short_url(update_request)
        print(f"Update response code: {update_response.code}")
        print(f"Update message: {update_response.message}")
        print()

        # Delete the short URL
        delete_request = DeleteShortUrlRequest(
            domain="s.ee",
            slug="example-update",
        )

        delete_response = await client.delete_short_url(delete_request)
        print(f"Delete response code: {delete_response.code}")
        print(f"Delete message: {delete_response.message}")
        print()


async def domains_and_tags_example(api_key: str) -> None:
    """Demonstrate getting available domains and tags."""
    print("=== Domains and Tags Example ===")
    print()

    async with SeeClient(api_key=api_key) as client:
        # Get available domains
        domains_response = await client.get_domains()
        print(f"Domains response code: {domains_response.code}")
        print(f"Available domains: {domains_response.data}")
        print()

        # Get available tags
        tags_response = await client.get_tags()
        print(f"Tags response code: {tags_response.code}")
        print(f"Available tags: {tags_response.data}")
        print()


async def error_handling_example(api_key: str) -> None:
    """Demonstrate error handling."""
    print("=== Error Handling Example ===")
    print()

    async with SeeClient(api_key=api_key) as client:
        # Handle validation errors
        try:
            # Missing domain validation
            empty_request = CreateShortUrlRequest(
                domain="",  # Empty domain will cause validation error
                target_url="not-a-valid-url",
            )
            await client.create_short_url(empty_request)
        except ValidationError as e:
            print(f"Validation error: {e}")
            print()

        # Handle authentication errors
        try:
            invalid_client = SeeClient(api_key="invalid-key-12345")
            async with invalid_client as invalid:
                request = CreateShortUrlRequest(
                    domain="s.ee",
                    target_url="https://example.com",
                )
                await invalid.create_short_url(request)
        except (AuthenticationError, APIError) as e:
            print(f"Authentication/API error: {e}")
            print()

        # Handle not found errors
        try:
            delete_request = DeleteShortUrlRequest(
                domain="s.ee",
                slug="nonexistent-slug-12345",
            )
            await client.delete_short_url(delete_request)
        except (NotFoundError, APIError) as e:
            print(f"Not found error: {e}")
            print()

        # Generic API error handling
        try:
            # Invalid target URL format
            bad_request = CreateShortUrlRequest(
                domain="s.ee",
                target_url="invalid-url-format",
            )
            await client.create_short_url(bad_request)
        except (ValidationError, APIError) as e:
            print(f"API error: {e}")
            print()


async def custom_configuration_example(api_key: str) -> None:
    """Demonstrate custom client configuration."""
    print("=== Custom Configuration Example ===")
    print()

    # Create client with custom settings
    client = SeeClient(
        api_key=api_key,
        base_url="https://s.ee/api",  # Custom API endpoint
        timeout=60.0,  # 60 seconds timeout
        max_retries=5,  # Retry failed requests up to 5 times
        proxy=None,  # Optional HTTP proxy
    )

    async with client:
        request = CreateShortUrlRequest(
            domain="s.ee",
            target_url="https://example.com/custom-config-test",
            title="Custom Config Test",
        )
        response = await client.create_short_url(request)
        print(f"Created with custom config - Code: {response.code}")
        print(f"Data: {response.data}")
        print()


async def batch_operations_example(api_key: str) -> None:
    """Demonstrate batch operations with async/await."""
    print("=== Batch Operations Example ===")
    print()

    urls_to_shorten = [
        ("https://example.com/page1", "batch-url-1"),
        ("https://example.com/page2", "batch-url-2"),
        ("https://example.com/page3", "batch-url-3"),
    ]

    async with SeeClient(api_key=api_key) as client:
        # Create multiple short URLs concurrently
        tasks = [
            client.create_short_url(
                CreateShortUrlRequest(
                    domain="s.ee",
                    target_url=url,
                    custom_slug=slug,
                    title=f"Batch URL {slug}",
                )
            )
            for url, slug in urls_to_shorten
        ]

        # Execute all requests concurrently
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        print("Created short URLs:")
        for (original, _), response in zip(urls_to_shorten, responses, strict=True):
            if isinstance(response, Exception):
                print(f"  {original} -> Error: {response}")
            else:
                print(f"  {original} -> Code: {response.code}, Data: {response.data}")
        print()


async def main() -> None:
    """Run all examples."""
    # Get API key from environment variable
    api_key = os.getenv("SEE_API_KEY")
    if not api_key:
        print("Error: Please set SEE_API_KEY environment variable")
        print("Usage: export SEE_API_KEY='your-api-key-here'")
        return

    examples = [
        ("Basic Usage", basic_usage_example),
        ("Custom Short URL", custom_short_url_example),
        ("Manage URLs (Update/Delete)", manage_urls_example),
        ("Domains and Tags", domains_and_tags_example),
        ("Error Handling", error_handling_example),
        ("Custom Configuration", custom_configuration_example),
        ("Batch Operations", batch_operations_example),
    ]

    for name, example_func in examples:
        try:
            await example_func(api_key)
        except Exception as e:
            print(f"{name} example failed: {e}\n")

    print("=== All Examples Complete ===")


if __name__ == "__main__":
    # Run the main async function
    asyncio.run(main())
