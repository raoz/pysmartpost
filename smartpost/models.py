from enum import Enum
import xml.etree.ElementTree as ET


class Recipient:

    def __init__(self, name, phone, email, to_pay=None, personal_id=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.to_pay = to_pay
        self.personal_id = personal_id

    def to_xml(self):
        el = ET.Element('recipient')
        ET.SubElement(el, "name").text = self.name
        ET.SubElement(el, "phone").text = self.phone
        ET.SubElement(el, "email").text = self.email
        if self.to_pay:
            ET.SubElement(el, "cash").text = str(self.to_pay)
        if self.personal_id:
            ET.SubElement(el, "idcode").text = self.personal_id

        return el


class Sender:

    def __init__(self, name, phone, email, to_pay, account):
        self.name = name
        self.phone = phone
        self.email = email
        self.to_pay = to_pay
        self.account = account

    def to_xml(self):
        el = ET.Element('sender')
        ET.SubElement(el, "name").text = self.name
        ET.SubElement(el, "phone").text = self.phone
        ET.SubElement(el, "email").text = self.email
        if self.to_pay:
            ET.SubElement(el, "cash").text = str(self.to_pay)
        if self.account:
            ET.SubElement(el, "account").text = self.account

        return el


class EEDestination:

    def __init__(self, place_id):
        self.place_id = place_id

    def to_xml(self):
        el = ET.Element("destination")
        ET.SubElement(el, "place_id").text = str(self.place_id)

        return el


class FIDestination:

    def __init__(self, postal_code, routing_code):
        self.postal_code = postal_code
        self.routing_code = routing_code

    def to_xml(self):
        el = ET.Element("destination")
        ET.SubElement(el, "postalcode").text = self.postal_code
        ET.SubElement(el, "routingcode").text = self.routing_code

        return el


class CourierDestination:
    class TimeWindow(Enum):
        ANY = 1
        WORKDAY = 2
        EVENING = 3

    def __init__(self, street, city, country, postal_code, details=None, time_window=TimeWindow.ANY, house=None,
                 apartment=None):
        self.street = street
        self.house = house
        self.apartment = apartment
        self.city = city
        self.country = country
        self.details = details
        self.time_window = time_window
        self.postal_code = postal_code

    def to_xml(self):
        el = ET.Element("destination")
        ET.SubElement(el, "street").text = self.street
        if self.house:
            ET.SubElement(el, "house").text = str(self.house)
        if self.apartment:
            ET.SubElement(el, "apartment").text = str(self.house)
        ET.SubElement(el, "city").text = self.city
        ET.SubElement(el, "country").text = self.country
        if self.details:
            ET.SubElement(el, "details").text = self.details
        ET.SubElement(el, "timewindow").text = str(self.time_window.value)
        ET.SubElement(el, "postalcode").text = str(self.postal_code)

        return el


class Item:
    class Size(Enum):
        XS = 11
        S = 5
        M = 6
        L = 7
        XL = 8

    def __init__(self, content, weight, size, destination, recipient, reference=None, sender=None,
                 barcode=None, parent_item=None, lq_items=None,
                 express=False, id_check=False, age_check=False, notify_email=None,
                 notify_phone=None, paid_by_recipient=False):
        self.reference = reference
        self.content = content
        self.weight = weight
        self.size = size
        self.sender = sender
        self.destination = destination
        self.recipient = recipient
        self.barcode = barcode
        self.parent_item = parent_item
        self.lq_items = lq_items
        self.additional_services = {
            "express": express,
            "idcheck": id_check,
            "agecheck": age_check,
            "notifyemail": notify_email,
            "notifyphone": notify_phone,
            "paidbyrecipient": paid_by_recipient
        }

    def to_xml(self):
        el = ET.Element("item")
        if self.barcode:
            ET.SubElement(el, "barcode").text = self.barcode
        ET.SubElement(el, "reference").text = self.reference
        ET.SubElement(el, "content").text = self.content
        if self.parent_item:
            ET.SubElement(el, "orderparent").text = self.parent_item.barcode
        ET.SubElement(el, "weight").text = str(self.weight)
        ET.SubElement(el, "size").text = str(self.size.value)
        if self.sender:
            el.append(self.sender.to_xml())
        el.append(self.recipient.to_xml())
        el.append(self.destination.to_xml())

        additional_services = ET.SubElement(el, "additionalservices")
        for k, v in self.additional_services.items():
            if v is not None:
                ET.SubElement(additional_services, k).text = str(v).lower()

        return el

    @staticmethod
    def mock():
        return Item(
            "1234",
            "Nothing",
            5,
            Item.Size.M,
            EEDestination(102),
            Recipient(
                "Heli Kopter",
                "+37255555555",
                "heli.kopter@example.com"
            )
        )


class SentItem:

    def __init__(self, barcode, reference, door_code=None):
        self.barcode = barcode
        self.reference = reference
        self.door_code = door_code

    def __repr__(self):
        return f"SentItem({self.barcode}, {self.reference}, {self.door_code}"

    def __str__(self):
        return self.__repr__()
