"""
Text sharing example for the SEE SDK.

This example demonstrates how to use the Text Sharing features of the SDK:
- Creating text snippets
- Updating text content
- Deleting text entries
- getting available text domains
"""

import asyncio
import os
from urllib.parse import urlparse

from see import SeeClient
from see.models import (
    CreateTextRequest,
    DeleteTextRequest,
    UpdateTextRequest,
)


async def main() -> None:
    # Get API key from environment variable
    api_key = os.getenv("SEE_API_KEY")
    if not api_key:
        print("Error: Please set SEE_API_KEY environment variable")
        return

    async with SeeClient(api_key=api_key) as client:
        print("=== Text Sharing Example ===")

        # 1. Get available text domains
        domains = await client.get_text_domains()
        print(f"Available text domains: {domains.data}")

        # 2. Create a new text snippet
        print("\nCreating text...")
        create_req = CreateTextRequest(
            content="Hello from SEE Python SDK!",
            title="My First SDK Text",
            # Optional parameters:
            # domain="t.see",      # Specify domain if needed
            # custom_slug="mysdk", # Custom URL slug
            # password="123",      # Password protection
            # expire_at=...,       # Expiration timestamp
        )
        created = await client.create_text(create_req)
        print(f"Created text: {created.short_url}")

        # 3. Update the text
        if created.short_url and created.slug:
            domain = urlparse(created.short_url).netloc
            print(f"\nUpdating text (slug: {created.slug}, domain: {domain})...")

            update_req = UpdateTextRequest(
                domain=domain,
                slug=created.slug,
                content="Updated content from Python SDK!",
                title="Updated Title",
            )
            updated = await client.update_text(update_req)
            print(f"Update status: {updated.code} - {updated.message}")

            # 4. Delete the text
            print("\nDeleting text...")
            delete_req = DeleteTextRequest(domain=domain, slug=created.slug)
            deleted = await client.delete_text(delete_req)
            print(f"Delete status: {deleted.code} - {deleted.message}")
        else:
            print("\nCannot update/delete: No short_url or slug returned.")


if __name__ == "__main__":
    asyncio.run(main())
