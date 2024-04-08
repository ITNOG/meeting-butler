"""
List of methods to interact with Eventbrite APIs
"""

import csv
import logging

import requests
from requests.exceptions import JSONDecodeError

from meeting_butler.user import User

LOGGER = logging.getLogger(__name__)


def get_registered_users(url: str) -> list[User]:
    """
    Retrieve a deuplicated list of registered users on Eventbrite.

    Arguments:
    ----------
    - url: str
      URL pointing to the Google doc share as CSV

    Returns:
    --------
    list[User]: Registered user
    """
    users = []
    LOGGER.debug("Fetching data for 123FormBuilder. URL: %s", url)
    request = requests.get(url, timeout=30)

    assert request.status_code == 200, f"Erroneous HTTP status code: {request.status_code}"

    try:
        content = request.content.decode("utf-8")
        attendees = csv.reader(content.splitlines(), delimiter=",")
    except (KeyError, JSONDecodeError) as error:
        raise ValueError(f"Malformed body: f{request.text}") from error

    for attendee in attendees:
        try:
            user = {
                "name": attendee[2].upper(),
                "surname": attendee[3].upper(),
                "company": attendee[4].upper(),
                "title": attendee[5].upper(),
                "email": attendee[6].upper(),
                "country": "IT",
            }

            if not user["company"]:
                # Empty company name
                user["company"] = f"{user['name']} {user['surname']}"

            asn = attendee[9]
            # Remove first "AS"
            if asn.upper().startswith("AS"):
                asn = asn[2:]
            try:
                user["asn"] = int(asn)
            except ValueError:
                user["asn"] = None
        except (TypeError, KeyError):
            logging.error("Malformatted row: %s", attendee)
            continue

        if user not in users:
            users.append(user)

    return users
