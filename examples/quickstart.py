"""
Simple quickstart example for the SEE URL SDK.

This example demonstrates the basic usage of the SEE URL SDK.
Make sure to set your API key as an environment variable before running:
    export SEE_API_KEY="your-api-key-here"
"""

import asyncio
import os

from see import SeeClient
from see.models import CreateShortUrlRequest


async def main() -> None:
    """Simple example showing basic SDK usage."""
    # Get API key from environment variable
    api_key = os.getenv("SEE_API_KEY")
    if not api_key:
        print("Error: Please set SEE_API_KEY environment variable")
        print("Usage: export SEE_API_KEY='your-api-key-here'")
        return

    # Initialize the client with your API key
    async with SeeClient(api_key=api_key) as client:
        # Create a short URL request
        request = CreateShortUrlRequest(
            domain="s.ee",  # Use your available domain
            target_url="https://example.com/very/long/url/that/needs/shortening",
            title="Example Short URL",
        )

        # Create the short URL
        response = await client.create_short_url(request)

        print(f"Success! Response code: {response.code}")
        print(f"Message: {response.message}")
        print(f"Short URL data: {response.data}")


if __name__ == "__main__":
    asyncio.run(main())
