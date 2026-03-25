# Migration Guide: Updating to New SmartPosti API

## Overview

SmartPosti (formerly Itella Smartpost) has updated their API infrastructure. This library now supports both the new and legacy authentication methods.

## What Changed?

### 1. API Endpoint
- **Old**: `https://iseteenindus.smartpost.ee/api/`
- **New**: `https://gateway.posti.fi/smartpost/api/ext/v1/`

### 2. Authentication Method
- **Old**: XML-embedded username/password
- **New**: HTTP Authorization header with API key

### 3. URL Structure
- **Old**: Request type sent as query parameter (`?request=shipment`)
- **New**: Request type in URL path (`/shipment`)

## How to Migrate

### Step 1: Get Your API Key

1. Log in to the [SmartPosti self-service portal](https://www.smartposti.ee/)
2. Navigate to Settings or API section
3. Generate a new API key
4. Save it securely (you can have two keys active during migration)

### Step 2: Update Your Code

**Before (Old Code):**
```python
from smartpost.api import SmartpostAPI

api = SmartpostAPI(
    username='your_username',
    password='your_password'
)
```

**After (New Code):**
```python
from smartpost.api import SmartpostAPI

api = SmartpostAPI(
    api_key='your-api-key-here'
)
```

### Step 3: Test Your Integration

The rest of the API remains the same:

```python
from smartpost.api import SmartpostAPI
from smartpost.models import Item, Recipient, EEDestination

# Initialize with new API key
api = SmartpostAPI(api_key='your-api-key')

# Create a shipment (same as before)
item = Item(
    content="Package contents",
    weight=1.5,
    size=Item.Size.M,
    destination=EEDestination(place_id=102),
    recipient=Recipient(
        name="John Doe",
        phone="+37255555555",
        email="john@example.com"
    ),
    reference="ORDER-12345"
)

sent_items = api.shipment([item])
```

## Backward Compatibility

If you need to use the old API temporarily (not recommended):

```python
api = SmartpostAPI(
    username='your_username',
    password='your_password',
    use_legacy_api=True  # Explicitly use old endpoint
)
```

**⚠️ Warning**: The legacy API is deprecated and may stop working at any time. Migrate to the new API as soon as possible.

## Troubleshooting

### Error: "Either api_key or username+password must be provided"
- You must provide authentication credentials. Use `api_key` for new API or `username`+`password` for legacy.

### Error: 401 Unauthorized
- Check that your API key is correct
- Ensure your API key is active in the self-service portal
- For legacy: verify username and password are correct

### Error: 404 Not Found
- The endpoint may have changed
- Verify you're not using `use_legacy_api=True` with an API key
- Check the official documentation for endpoint changes

## Additional Resources

- [SmartPosti API Documentation v1.71](https://assets.ctfassets.net/dvxpcmq06s7e/xxWIO89f2XuBvAvOZoDjs/9010f707b98ce3deed9f44cc701a1219/smartposti-api-documentation-171.pdf)
- [SmartPosti Developer Portal](https://www.smartposti.ee/en/for-businesses/client-service/download-modules)
- [Legacy Documentation](https://uus.smartpost.ee/ariklient/ostukorvi-rippmenuu-lisamise-opetus/automaatse-andmevahetuse-opetus) (may be outdated)

## Support

If you encounter issues:
1. Check the official SmartPosti API documentation
2. Verify your credentials in the self-service portal
3. Contact SmartPosti support for API-specific issues
4. Open an issue on this repository for library-related problems
