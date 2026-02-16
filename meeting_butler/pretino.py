"""
List of methods to interact with the Pretino API
"""

import logging

import requests
from pydantic import TypeAdapter
from requests.exceptions import JSONDecodeError

from meeting_butler.user import User

LOGGER = logging.getLogger(__name__)


def get_registered_users(url: str, api_key: str) -> list[User]:
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
    LOGGER.debug("Fetching data for Pretino. URL: %s", url)
    request = requests.get(url, timeout=30, headers={"x-pretino-key": api_key})

    assert request.status_code == 200, f"Erroneous HTTP status code: {request.status_code}"

    try:
        attendees = request.json()
        # Check that response is a list of dictionaries
        validator = TypeAdapter(list[dict])
        validator.validate_python(request.json())
    except (KeyError, JSONDecodeError) as error:
        raise ValueError(f"Malformed body: f{request.text}") from error

    for attendee in attendees:
        try:
            user = {
                "name": attendee["name"].upper(),
                "surname": attendee["surname"].upper(),
                "company": attendee["company"].upper(),
                "title": attendee["job_title"].upper(),
                "email": attendee["email"].upper(),
                "country": "IT",
            }

            if not user["company"]:
                # Empty company name
                user["company"] = f'{user["name"]} {user["surname"]}'

            asn = attendee["asn"]
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
