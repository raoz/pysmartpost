# pysmartpost
Python library to create [SmartPosti (formerly Itella Smartpost)](https://www.smartposti.ee/) parcels programmatically.

## ⚠️ Important: API Update

SmartPosti has updated their API. **The old username/password authentication is deprecated.** Please migrate to the new API key authentication. See [MIGRATION.md](MIGRATION.md) for details.

## Installation

```bash
pip install smartpost
```

## Quick Start

### New API (Recommended)
Use API key authentication with the new SmartPosti API:

```python
from smartpost.api import SmartpostAPI
from smartpost.models import Item, Recipient, EEDestination

# Initialize with API key
api = SmartpostAPI(api_key='your-api-key-here')

# Create a shipment
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
print(f"Barcode: {sent_items[0].barcode}")
```

**Get your API key** from the [SmartPosti self-service portal](https://www.smartposti.ee/).

### Legacy API (Deprecated - Not Recommended)
The old XML-based authentication is deprecated and may stop working at any time:

```python
api = SmartpostAPI(
    username='your-username', 
    password='your-password', 
    use_legacy_api=True
)
```

## Migration Guide

If you're upgrading from an older version, see [MIGRATION.md](MIGRATION.md) for a complete migration guide.

## Documentation

- **Current API Documentation (v1.71)**: [Download PDF](https://assets.ctfassets.net/dvxpcmq06s7e/xxWIO89f2XuBvAvOZoDjs/9010f707b98ce3deed9f44cc701a1219/smartposti-api-documentation-171.pdf)
- **SmartPosti Developer Resources**: [https://www.smartposti.ee/en/for-businesses/client-service/download-modules](https://www.smartposti.ee/en/for-businesses/client-service/download-modules)
- **Legacy Documentation** (outdated): [Link](https://uus.smartpost.ee/ariklient/ostukorvi-rippmenuu-lisamise-opetus/automaatse-andmevahetuse-opetus)

## Features

- ✅ Support for new SmartPosti API with API key authentication
- ✅ Backward compatibility with legacy authentication (deprecated)
- ✅ Create shipments programmatically
- ✅ Generate shipping labels
- ✅ Support for Estonia (EE), Finland (FI), Latvia (LV), and Lithuania (LT)
- ✅ Multiple destination types: parcel terminals, courier delivery
- ✅ Additional services: express, ID check, age check, COD

## License

MIT License - see LICENSE file for details.

