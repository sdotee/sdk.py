"""
File sharing example for the SEE SDK.

This example demonstrates how to use the File Sharing features of the SDK:
- Uploading files
- Deleting files
- Getting available file domains
"""

import asyncio
import contextlib
import os
import tempfile
from pathlib import Path

from see import SeeClient


async def main() -> None:
    # Get API key from environment variable
    api_key = os.getenv("SEE_API_KEY")
    if not api_key:
        print("Error: Please set SEE_API_KEY environment variable")
        return

    async with SeeClient(api_key=api_key) as client:
        print("=== File Sharing Example ===")

        # 1. Get available file domains
        domains = await client.get_file_domains()
        print(f"Available file domains: {domains.data}")

        # Create a dummy file for demonstration
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
            tmp.write("This is a test file uploaded via SEE Python SDK.")
            tmp_path = tmp.name

        try:
            # 2. Upload the file
            print(f"\nUploading file: {tmp_path}")
            uploaded = await client.upload_file(tmp_path)

            print("Upload successful!")
            print(f"URL: {uploaded.url}")
            print(f"Hash: {uploaded.hash}")
            print(f"Size: {uploaded.size} bytes")

            # 3. Delete the file
            if uploaded.hash:
                print(f"\nDeleting file with hash: {uploaded.hash}")
                deleted = await client.delete_file(uploaded.hash)
                print(f"Delete status: {deleted.code} - {deleted.message}")

        finally:
            # Cleanup temporary file
            with contextlib.suppress(OSError):
                Path(tmp_path).unlink()


if __name__ == "__main__":
    asyncio.run(main())
