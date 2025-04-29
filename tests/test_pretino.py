import copy
import unittest

import responses

from meeting_butler.pretino import get_registered_users

RESPONSE = {
    "method": responses.GET,
    "url": ("http://www.example.com/pretino/orders/"),
    "body": """
        [
            {
                "name": "PC",
                "surname": "Principal",
                "company": "South Park Elementary School",
                "asn": "AS0",
                "job_title": "School Principal",
                "email": "pcprincipal@example.com",
                "order_id": "some_random_string",
                "bio_url": "https://www.linkedin.com/pcprincipal",
                "tshirt_size": "XL",
                "qrcode": "54321"
            },
            {
                "name": "Strong",
                "surname": "Woman",
                "company": "South Park Elementary School",
                "asn": "AS65535",
                "job_title": "Teacher",
                "email": "strongwoman@example.com",
                "order_id": "other_random_string",
                "bio_url": "https://www.linkedin.com/strongwoman",
                "tshirt_size": "M",
                "qrcode": "12345"
            }
        ]
    """,
    "status": 200,
    "content_type": "application/json",
}


class TestCase(unittest.TestCase):
    @responses.activate
    def test_wrong_http_status(self):
        response = copy.copy(RESPONSE)
        response["status"] = 404
        responses.add(**response)

        with self.assertRaises(AssertionError):
            registered_users = get_registered_users(
                "http://www.example.com/pretino/orders/", "TOKEN"
            )
            list(registered_users)

    @responses.activate
    def test_non_json_body(self):
        response = copy.copy(RESPONSE)
        response["body"] = "-->WRONG<--"
        responses.add(**response)

        with self.assertRaises(ValueError):
            registered_users = get_registered_users(
                "http://www.example.com/pretino/orders/", "TOKEN"
            )
            list(registered_users)

    @responses.activate
    def test_malformed_json_body(self):
        response = copy.copy(RESPONSE)
        response["body"] = '{"foo": []}'
        responses.add(**response)

        with self.assertRaises(ValueError):
            registered_users = get_registered_users(
                "http://www.example.com/pretino/orders/", "TOKEN"
            )
            list(registered_users)

    @responses.activate
    def test_succesful_request(self):
        responses.add(**RESPONSE)

        registered_users = get_registered_users("http://www.example.com/pretino/orders/", "TOKEN")
        self.assertListEqual(
            list(registered_users),
            [
                {
                    "name": "PC",
                    "surname": "PRINCIPAL",
                    "company": "SOUTH PARK ELEMENTARY SCHOOL",
                    "email": "PCPRINCIPAL@EXAMPLE.COM",
                    "title": "SCHOOL PRINCIPAL",
                    "asn": 0,
                    "country": "IT",
                },
                {
                    "name": "STRONG",
                    "surname": "WOMAN",
                    "company": "SOUTH PARK ELEMENTARY SCHOOL",
                    "email": "STRONGWOMAN@EXAMPLE.COM",
                    "title": "TEACHER",
                    "asn": 65535,
                    "country": "IT",
                },
            ],
        )
