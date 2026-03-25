import xml.etree.ElementTree as ET

import requests

from .errors import SmartpostError
from .models import SentItem


class SmartpostAPI:

    def __init__(self, username=None, password=None, api_key=None,
                 session=None, timeout=30, proxies=None, use_legacy_api=False):
        """
        Initialize SmartpostAPI client.
        
        Args:
            username: (Deprecated) Username for legacy XML authentication
            password: (Deprecated) Password for legacy XML authentication
            api_key: API key for new authentication method (recommended)
            session: Optional requests.Session instance
            timeout: Request timeout in seconds
            proxies: Optional proxy configuration
            use_legacy_api: If True, uses old endpoint (deprecated, not recommended)
        
        Note:
            The new API uses API key authentication via Authorization header.
            Old username/password XML authentication is deprecated.
            Get your API key from: https://www.smartposti.ee/
        """
        if use_legacy_api:
            self.BASE_URL = "https://iseteenindus.smartpost.ee/api/"
        else:
            self.BASE_URL = "https://gateway.posti.fi/smartpost/api/ext/v1/"
        
        self.username = username
        self.password = password
        self.api_key = api_key
        self.use_legacy_auth = bool(username and password and not api_key)
        self.session = session or requests.Session()
        self.timeout = timeout
        self.proxies = proxies
        
        if not self.use_legacy_auth and not self.api_key:
            raise ValueError(
                "Either api_key (recommended) or username+password (deprecated) must be provided"
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        self.session.close()

    def post(self, request, document, return_format='text'):
        # Prepare headers
        headers = {'Content-Type': 'application/xml'}
        
        # Add authentication based on method
        if self.use_legacy_auth:
            # Old XML-based authentication (deprecated)
            auth = ET.Element('authentication')
            user = ET.SubElement(auth, "user")
            password = ET.SubElement(auth, "password")
            user.text = self.username
            password.text = self.password
            document.insert(0, auth)
        else:
            # New API key authentication via header
            headers['Authorization'] = self.api_key

        xml = ET.tostring(document)
        print(xml)

        # Build URL with request parameter for legacy API, or use endpoint path for new API
        if self.use_legacy_auth:
            url = f"{self.BASE_URL}"
            params = {'request': request}
        else:
            # For new API, the request type is part of the URL path
            url = f"{self.BASE_URL}{request}"
            params = {}

        r = self.session.post(
            url,
            params=params,
            data=xml,
            headers=headers,
            timeout=self.timeout,
            proxies=self.proxies,
        )
        if r.ok:
            if return_format == 'text':
                return r.text
            elif return_format == 'bytes':
                return r.content
            else:
                raise ValueError("Invalid format")
        else:
            print(r.status_code)
            raise SmartpostError(r.text)

    def labels(self, label_format, *barcodes):
        allowed_formats = ["A5", "A6", "A6-4", "A7", "A7-8"]
        if label_format not in allowed_formats:
            raise ValueError(f"Format must be one of {','.join(allowed_formats)}")

        doc = ET.Element("labels")
        format_el = ET.SubElement(doc, "format")
        format_el.text = label_format

        for barcode in barcodes:
            barcode_el = ET.SubElement(doc, "barcode")
            barcode_el.text = barcode

        return self.post("labels", doc, "bytes")

    def shipment(self, items, report_emails=[]):
        if len(report_emails) > 5:
            raise ValueError("Can have no more than five report fiels")

        doc = ET.Element("orders")
        report = ET.SubElement(doc, "report")
        for report_email in report_emails:
            ET.SubElement(report, "email").text = report_email

        for item in items:
            doc.append(item.to_xml())

        response_xml = self.post("shipment", doc)
        response_data = ET.fromstring(response_xml)

        sent_items = []
        for item_data in response_data:
            sender_code = None
            if item_data.find("sender"):
                sender_code = item_data.find("sender").find("doorcode").text
            sent_items.append(SentItem(
                item_data.find("barcode").text,
                item_data.find("reference").text,
                sender_code
            ))

        return sent_items

