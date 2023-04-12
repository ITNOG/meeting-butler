import copy
import unittest

import responses

from meeting_butler.eventbrite import get_registered_users

RESPONSE = {
    "method": responses.GET,
    "url": ("https://www.eventbriteapi.com/v3/events/" "EVENT/attendees/?token=TOKEN&page=1"),
    "body": """
        {
            "pagination": {
                "page_count": 1
            },
            "attendees": [
                {
                    "cancelled": false,
                    "profile": {
                        "first_name": "Marco",
                        "last_name": "Marzetti",
                        "company": "ITNOG",
                        "email": "marco@itnog.it",
                        "job_title": "Kodamas Tamer"
                     },
                     "answers": [
                        {
                            "question": "ASN",
                            "answer": "64496"
                        }
                    ]
                },
                {
                    "cancelled": true,
                    "profile": {
                        "first_name": "Paolo",
                        "last_name": "Lucente",
                        "company": "ITNOG",
                        "email": "paolo@itnog.it",
                        "job_title": "Fa cose e vede gente"
                     },
                     "answers": [
                        {
                            "question": "ASN",
                            "answer": "64496"
                        }
                    ]
                }
            ]
        }
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
            registered_users = get_registered_users("EVENT", "TOKEN")
            list(registered_users)

    @responses.activate
    def test_non_json_body(self):
        response = copy.copy(RESPONSE)
        response["body"] = "-->WRONG<--"
        responses.add(**response)

        with self.assertRaises(ValueError):
            registered_users = get_registered_users("EVENT", "TOKEN")
            list(registered_users)

    @responses.activate
    def test_malformed_json_body(self):
        response = copy.copy(RESPONSE)
        response["body"] = '{"foo": []}'
        responses.add(**response)

        with self.assertRaises(ValueError):
            registered_users = get_registered_users("EVENT", "TOKEN")
            list(registered_users)

    @responses.activate
    def test_succesful_request(self):
        responses.add(**RESPONSE)

        registered_users = get_registered_users("EVENT", "TOKEN")
        self.assertListEqual(
            list(registered_users),
            [
                {
                    "name": "MARCO",
                    "surname": "MARZETTI",
                    "company": "ITNOG",
                    "email": "MARCO@ITNOG.IT",
                    "title": "KODAMAS TAMER",
                    "asn": 64496,
                }
            ],
        )
