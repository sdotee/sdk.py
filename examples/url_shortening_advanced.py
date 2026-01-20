"""
Advanced example demonstrating complex workflows with the SEE URL SDK.

This example shows:
- Creating multiple URLs with tags
- Managing tags and domains
- Custom URL configurations
- Using environment variables for configuration

Make sure to set your API key as an environment variable before running:
    export SEE_API_KEY="your-api-key-here"
"""

import asyncio
import os
from datetime import datetime, timedelta

from see import SeeClient
from see.models import CreateShortUrlRequest


async def get_available_resources(api_key: str) -> None:
    """Demonstrate getting available domains and tags before creating URLs."""
    print("=== Getting Available Resources ===")
    print()

    async with SeeClient(api_key=api_key) as client:
        # Get available domains
        domains = await client.get_domains()
        print(f"Available domains (Code: {domains.code}):")
        if domains.data:
            for key, domain_list in domains.data.items():
                print(f"  {key}: {domain_list}")
        print()

        # Get available tags
        tags = await client.get_tags()
        print(f"Available tags (Code: {tags.code}):")
        if tags.data:
            for key, tag_list in tags.data.items():
                print(f"  {key}: {tag_list}")
        print()


async def create_campaign_urls(api_key: str) -> None:
    """Create multiple URLs for a marketing campaign."""
    print("=== Creating Campaign URLs ===")
    print()

    async with SeeClient(api_key=api_key) as client:
        # Define campaign URLs
        campaigns = [
            {
                "name": "Email Campaign",
                "url": "https://example.com/landing/email-promo",
                "slug": "email-promo-2025",
                "tag_ids": [1],
            },
            {
                "name": "Social Media Campaign",
                "url": "https://example.com/landing/social-promo",
                "slug": "social-promo-2025",
                "tag_ids": [2],
            },
            {
                "name": "Newsletter Campaign",
                "url": "https://example.com/landing/newsletter",
                "slug": "newsletter-2025",
                "tag_ids": [1, 2],
            },
        ]

        # Create all campaign URLs
        for campaign in campaigns:
            request = CreateShortUrlRequest(
                domain="s.ee",
                target_url=campaign["url"],
                custom_slug=campaign["slug"],
                title=campaign["name"],
                tag_ids=campaign["tag_ids"],
            )

            try:
                response = await client.create_short_url(request)
                print(f"✓ Created: {campaign['name']}")
                print(f"  Slug: {campaign['slug']}")
                print(f"  Response: {response.data}")
                print()
            except Exception as e:
                print(f"✗ Failed: {campaign['name']} - {e}")
                print()


async def create_expiring_urls(api_key: str) -> None:
    """Create URLs with different expiration times."""
    print("=== Creating Expiring URLs ===")
    print()

    async with SeeClient(api_key=api_key) as client:
        now = datetime.now()

        # Create URLs with different expiration times
        expiring_urls = [
            {
                "title": "1 Hour Expiry",
                "days": 1 / 24,
                "url": "https://example.com/flash-sale-1h",
                "slug": "flash-1h",
            },
            {
                "title": "7 Days Expiry",
                "days": 7,
                "url": "https://example.com/weekly-offer",
                "slug": "week-offer",
            },
            {
                "title": "30 Days Expiry",
                "days": 30,
                "url": "https://example.com/monthly-deal",
                "slug": "month-deal",
            },
        ]

        for config in expiring_urls:
            expire_time = now + timedelta(days=config["days"])
            expire_timestamp = int(expire_time.timestamp())

            request = CreateShortUrlRequest(
                domain="s.ee",
                target_url=config["url"],
                custom_slug=config["slug"],
                title=config["title"],
                expire_at=expire_timestamp,
                expiration_redirect_url="https://example.com/expired",
            )

            try:
                response = await client.create_short_url(request)
                print(f"✓ Created: {config['title']}")
                print(f"  Expires: {expire_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  Data: {response.data}")
                print()
            except Exception as e:
                print(f"✗ Failed: {config['title']} - {e}")
                print()


async def create_password_protected_urls(api_key: str) -> None:
    """Create password-protected short URLs."""
    print("=== Creating Password-Protected URLs ===")
    print()

    async with SeeClient(api_key=api_key) as client:
        # Create a password-protected URL
        request = CreateShortUrlRequest(
            domain="s.ee",
            target_url="https://example.com/secret/content",
            custom_slug="secret-content",
            title="Password Protected Content",
            password="secure123",  # Note: In production, use strong passwords
        )

        try:
            response = await client.create_short_url(request)
            print("✓ Created password-protected URL")
            print(f"  Password: {request.password}")
            print(f"  Data: {response.data}")
            print("  Note: Users will need to enter the password to access the URL")
            print()
        except Exception as e:
            print(f"✗ Failed to create password-protected URL: {e}")
            print()


async def workflow_example(api_key: str) -> None:
    """Demonstrate a complete workflow: create, update, then delete."""
    print("=== Complete Workflow Example ===")
    print()

    async with SeeClient(api_key=api_key) as client:
        # Step 1: Create a URL
        print("Step 1: Creating short URL...")
        create_request = CreateShortUrlRequest(
            domain="s.ee",
            target_url="https://example.com/workflow-test",
            custom_slug="workflow-demo",
            title="Workflow Demo URL",
        )

        create_response = await client.create_short_url(create_request)
        print(f"  Created: {create_response.data}")
        print()

        # Step 2: Wait a moment
        print("Step 2: Waiting for 1 second...")
        await asyncio.sleep(1)
        print()

        # Step 3: Update the URL
        print("Step 3: Updating the URL...")
        from see.models import UpdateShortUrlRequest

        update_request = UpdateShortUrlRequest(
            domain="s.ee",
            slug="workflow-demo",
            target_url="https://example.com/workflow-updated",
            title="Updated Workflow Demo",
        )

        update_response = await client.update_short_url(update_request)
        print(
            f"  Updated: Code {update_response.code}, Message: {update_response.message}"
        )
        print()

        # Step 4: Delete the URL
        print("Step 4: Cleaning up - deleting the URL...")
        from see.models import DeleteShortUrlRequest

        delete_request = DeleteShortUrlRequest(
            domain="s.ee",
            slug="workflow-demo",
        )

        delete_response = await client.delete_short_url(delete_request)
        print(
            f"  Deleted: Code {delete_response.code}, Message: {delete_response.message}"
        )
        print()


async def main() -> None:
    """Run all advanced examples."""
    # Get API key from environment variable
    api_key = os.getenv("SEE_API_KEY")
    if not api_key:
        print("Error: Please set SEE_API_KEY environment variable")
        print("Usage: export SEE_API_KEY='your-api-key-here'")
        return

    examples = [
        ("Available Resources", get_available_resources),
        ("Campaign URLs", create_campaign_urls),
        ("Expiring URLs", create_expiring_urls),
        ("Password-Protected URLs", create_password_protected_urls),
        ("Complete Workflow", workflow_example),
    ]

    for name, example_func in examples:
        try:
            await example_func(api_key)
        except Exception as e:
            print(f"{name} example failed: {e}\n")

    print("=== All Advanced Examples Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
