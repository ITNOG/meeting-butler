"""
List of methods to interact with Eventbrite APIs
"""

import logging
from urllib.parse import urlencode

import requests
from requests.exceptions import JSONDecodeError

from meeting_butler.user import User

LOGGER = logging.getLogger(__name__)


def get_registered_users(event: str, token: str) -> list[User]:
    """
    Retrieve a deuplicated list of registered users on Eventbrite.

    Arguments:
    ----------
    - event: str
      Eventbrite event ID
    - token: str
      Eventbrite API token ID

    Returns:
    --------
    list[User]: Registered user
    """
    url = f"https://www.eventbriteapi.com/v3/events/{event}/attendees/"

    users = []
    page = 1
    while True:
        params = urlencode({"token": token, "page": page})
        request_url = f"{url}?{params}"
        LOGGER.debug("Fetching data for eventbrite. Event: %s, Page: %d", event, page)
        request = requests.get(request_url, timeout=30)

        assert request.status_code == 200, f"Erroneous HTTP status code: {request.status_code}"

        try:
            body = request.json()
            attendees = body["attendees"]
            pages = body["pagination"]["page_count"]
        except (KeyError, JSONDecodeError) as error:
            raise ValueError(f"Malformed body: f{request.text}") from error

        for attendee in attendees:
            if attendee["cancelled"]:
                continue

            try:
                user = {
                    "name": attendee["profile"]["first_name"].upper(),
                    "surname": attendee["profile"]["last_name"].upper(),
                    "company": attendee["profile"]["company"].upper(),
                    "email": attendee["profile"]["email"].upper(),
                    "title": attendee["profile"]["job_title"].upper(),
                }

                asn = next(
                    iter(
                        [
                            answer["answer"]
                            for answer in attendee["answers"]
                            if answer["question"] == "ASN"
                        ]
                    )
                )
                # Remove first "AS"
                if asn.upper().startswith("AS"):
                    asn = asn[2:]
                try:
                    user["asn"] = int(asn)
                except ValueError:
                    user["asn"] = None
            except (TypeError, KeyError):
                logging.error("Malformatted object: %s", attendee)
                continue

            if user not in users:
                users.append(user)

        if page >= pages:
            break
        page += 1

    return users
