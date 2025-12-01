# SEE URL SDK Examples

This directory contains example code demonstrating how to use the SEE URL Python SDK.

## Setup

Before running any examples, make sure you have:

1. **Installed the SDK**:
   ```bash
   pip install -e ..
   ```

2. **Set your API key** as an environment variable:
   ```bash
   export SEE_API_KEY="your-api-key-here"
   ```

   **Security Note**: Never hardcode API keys in your source code. Always use environment variables or secure configuration management.

## Examples

### 1. quickstart.py

The simplest example showing basic SDK usage.

**What it demonstrates**:
- Creating a basic short URL
- Using environment variables for API keys
- Basic error handling

**Run it**:
```bash
python quickstart.py
```

### 2. complete_example.py

Comprehensive example covering all major SDK features.

**What it demonstrates**:
- Creating basic short URLs
- Creating custom short URLs with advanced options
- Updating and deleting URLs
- Getting available domains and tags
- Error handling (validation, authentication, not found)
- Custom client configuration
- Batch operations with async/await

**Run it**:
```bash
python complete_example.py
```

### 3. advanced_example.py

Advanced workflows and use cases.

**What it demonstrates**:
- Getting available resources (domains and tags)
- Creating campaign URLs with tags
- Creating URLs with expiration times
- Password-protected URLs
- Complete workflow (create → update → delete)

**Run it**:
```bash
python advanced_example.py
```

## Environment Variables

| Variable      | Required | Description                     | Example               |
| ------------- | -------- | ------------------------------- | --------------------- |
| `SEE_API_KEY` | Yes      | Your API key for authentication | `sk_1234567890abcdef` |

## Common Use Cases

### Creating a Simple Short URL

```python
import asyncio
import os
from see import SeeClient
from see.models import CreateShortUrlRequest

async def main():
    api_key = os.getenv("SEE_API_KEY")
    
    async with SeeClient(api_key=api_key) as client:
        request = CreateShortUrlRequest(
            domain="s.ee",
            target_url="https://example.com/my-long-url",
            title="My Short URL"
        )
        response = await client.create_short_url(request)
        print(f"Short URL created: {response.data}")

asyncio.run(main())
```

### Creating a Custom Short URL with Expiration

```python
from datetime import datetime, timedelta

expire_time = datetime.now() + timedelta(days=7)
expire_timestamp = int(expire_time.timestamp())

request = CreateShortUrlRequest(
    domain="s.ee",
    target_url="https://example.com/limited-offer",
    custom_slug="summer-sale",
    title="Summer Sale",
    expire_at=expire_timestamp,
    expiration_redirect_url="https://example.com/offers"
)
```

### Creating a Password-Protected URL

```python
request = CreateShortUrlRequest(
    domain="s.ee",
    target_url="https://example.com/private-content",
    custom_slug="private",
    password="secure-password",
    title="Private Content"
)
```

### Batch Creating Multiple URLs

```python
urls = [
    ("https://example.com/page1", "page-1"),
    ("https://example.com/page2", "page-2"),
    ("https://example.com/page3", "page-3"),
]

async with SeeClient(api_key=api_key) as client:
    tasks = [
        client.create_short_url(
            CreateShortUrlRequest(
                domain="s.ee",
                target_url=url,
                custom_slug=slug
            )
        )
        for url, slug in urls
    ]
    
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    for response in responses:
        if isinstance(response, Exception):
            print(f"Error: {response}")
        else:
            print(f"Created: {response.data}")
```

## Error Handling

All examples include proper error handling. The SDK raises these exceptions:

- `ValidationError`: Invalid input data (empty domain, invalid URL format)
- `AuthenticationError`: Invalid or missing API key
- `NotFoundError`: Resource not found (URL doesn't exist)
- `RateLimitError`: Too many requests
- `APIError`: General API errors

Example:

```python
from see.exceptions import ValidationError, APIError

try:
    response = await client.create_short_url(request)
except ValidationError as e:
    print(f"Invalid input: {e}")
except APIError as e:
    print(f"API error: {e}")
```

## Best Practices

1. **Always use environment variables** for sensitive data like API keys
2. **Use async context managers** (`async with`) to ensure proper cleanup
3. **Handle exceptions** appropriately in production code
4. **Use custom slugs wisely** - they must be unique per domain
5. **Set expiration times** for temporary URLs
6. **Use tags** to organize and categorize your URLs
7. **Enable retry logic** in production (configured in client initialization)

## Troubleshooting

### "Please set SEE_API_KEY environment variable"

Make sure you've set the environment variable:
```bash
export SEE_API_KEY="your-api-key"
```

Or set it inline:
```bash
SEE_API_KEY="your-api-key" python quickstart.py
```

### "ValidationError: API key is required"

Your API key is empty or not set. Check your environment variable.

### "ValidationError: Invalid URL"

The target URL must start with `http://` or `https://`.

### "APIError: Custom slug already exists"

The custom slug you chose is already taken. Try a different one or omit it to get an auto-generated slug.

## More Information

- [SDK Documentation](../README.md)
- [API Reference](https://s.ee/docs)
- [GitHub Repository](https://github.com/yourusername/see-python-sdk)

## Support

If you encounter issues or have questions:
- Check the [main README](../README.md)
- Open an issue on GitHub
- Review the API documentation
