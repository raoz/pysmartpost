# pysmartpost
Python library to create [SmartPosti (formerly Itella Smartpost)](https://www.smartposti.ee/) parcels programmatically.

## Authentication

The library supports both the **new API key authentication** (recommended) and the legacy username/password authentication (deprecated).

### New API (Recommended)
Use API key authentication with the new SmartPosti API:

```python
from smartpost.api import SmartpostAPI

api = SmartpostAPI(api_key='your-api-key-here')
```

Get your API key from the [SmartPosti self-service portal](https://www.smartposti.ee/).

### Legacy API (Deprecated)
The old XML-based authentication is deprecated and may stop working at any time:

```python
api = SmartpostAPI(username='your-username', password='your-password', use_legacy_api=True)
```

**Migration:** Update your code to use API keys as soon as possible.

## Documentation

- **Current API Documentation (v1.71)**: [Download PDF](https://assets.ctfassets.net/dvxpcmq06s7e/xxWIO89f2XuBvAvOZoDjs/9010f707b98ce3deed9f44cc701a1219/smartposti-api-documentation-171.pdf)
- **SmartPosti Developer Resources**: [https://www.smartposti.ee/en/for-businesses/client-service/download-modules](https://www.smartposti.ee/en/for-businesses/client-service/download-modules)

Communication is via XML. For older documentation, see the [legacy API reference](https://uus.smartpost.ee/ariklient/ostukorvi-rippmenuu-lisamise-opetus/automaatse-andmevahetuse-opetus) (may be outdated).

