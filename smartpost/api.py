import xml.etree.ElementTree as ET

import requests

from .errors import SmartpostError
from .models import SentItem


class SmartpostAPI:

    def __init__(self, username, password,
                 session=None, timeout=30, proxies=None):
        self.BASE_URL = "https://iseteenindus.smartpost.ee/api/"
        self.username = username
        self.password = password
        self.session = session or requests.Session()
        self.timeout = timeout
        self.proxies = proxies

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        self.session.close()

    def post(self, request, document, return_format='text'):
        auth = ET.Element('authentication')
        user = ET.SubElement(auth, "user")
        password = ET.SubElement(auth, "password")
        user.text = self.username
        password.text = self.password

        document.insert(0, auth)

        xml = ET.tostring(document)
        print(xml)

        r = self.session.post(
            f"{self.BASE_URL}",
            params={
                'request': request,
            },
            data=xml,
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

