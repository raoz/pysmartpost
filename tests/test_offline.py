"""Offline unit tests: no network access or credentials required."""
import xml.etree.ElementTree as ET
from unittest import mock

import pytest

from smartpost.api import SmartpostAPI
from smartpost.errors import SmartpostError
from smartpost.models import EEDestination, Item, Recipient


def make_api(response_text="", ok=True, content=b""):
    session = mock.Mock()
    session.post.return_value = mock.Mock(ok=ok, text=response_text, content=content, status_code=200 if ok else 400)
    return SmartpostAPI(api_key="dummy-key", session=session), session


def test_requires_credentials():
    with pytest.raises(ValueError):
        SmartpostAPI(session=mock.Mock())


def test_new_api_uses_authorization_header():
    api, session = make_api(content=b"%PDF")
    assert api.labels("A6", "123") == b"%PDF"
    _, kwargs = session.post.call_args
    assert session.post.call_args[0][0] == "https://gateway.posti.fi/smartpost/api/ext/v1/labels"
    assert kwargs["headers"]["Authorization"] == "dummy-key"


def test_legacy_api_embeds_authentication():
    session = mock.Mock()
    session.post.return_value = mock.Mock(ok=True, content=b"x")
    api = SmartpostAPI(username="u", password="p", session=session, use_legacy_api=True)
    api.labels("A5", "1")
    _, kwargs = session.post.call_args
    assert kwargs["params"] == {"request": "labels"}
    doc = ET.fromstring(kwargs["data"])
    assert doc.find("authentication/user").text == "u"


def test_invalid_label_format():
    api, _ = make_api()
    with pytest.raises(ValueError):
        api.labels("A4", "123")


def test_error_response_raises():
    api, _ = make_api(response_text="bad", ok=False)
    with pytest.raises(SmartpostError):
        api.labels("A6", "123")


def test_item_to_xml():
    item = Item(
        "Books", 1.5, Item.Size.M, EEDestination(102),
        Recipient("Heli Kopter", "+37255555555", "heli.kopter@example.com"),
        reference="ref-1",
    )
    el = item.to_xml()
    assert el.find("reference").text == "ref-1"
    assert el.find("size").text == "6"
    assert el.find("destination/place_id").text == "102"
    assert el.find("additionalservices/express").text == "false"


def test_shipment_parses_response():
    response = "<orders><item><barcode>BC1</barcode><reference>ref-1</reference></item></orders>"
    api, _ = make_api(response_text=response)
    item = Item("Books", 1, Item.Size.S, EEDestination(1), Recipient("A", "1", "a@example.com"), reference="ref-1")
    sent = api.shipment([item])
    assert sent[0].barcode == "BC1"
    assert sent[0].reference == "ref-1"
