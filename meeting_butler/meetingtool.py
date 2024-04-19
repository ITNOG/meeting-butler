"""
Methods to interact with NIX.CZ's meetingtool
"""

import json
import logging
from time import sleep

import requests

from meeting_butler.user import User

LOGGER = logging.getLogger(__name__)


def register_users(hostname: str, token: str, users: list[User]) -> None:
    """
    Register users on meetingtool

    Arguments:
    ----------
    hostname: str
        Instance hostname
    token: str
        API auth token
    users: list[Users]
        List of users that shall be registered
    """
    url = f"https://{hostname}/api/registrations/import/"
    headers = {"Authorization": f"Bearer {token}"}

    LOGGER.info("Importing: %d users", len(users))

    for user in users:
        data = [
            {
                "firstName": user["name"],
                "lastName": user["surname"],
                "company": user["company"],
                # Email address has to be lowercase
                "mail": user["email"].lower(),
                "jobTitle": user["title"],
                "asn": user["asn"],
                "countryCode": user["country"],
                "companyCountryCode": user["country"],
            }
        ]

        LOGGER.debug("Importing the following users: %s", data)
        response = requests.post(url, data=json.dumps(data), headers=headers, timeout=30)

        status = response.status_code
        if status != 200:
            error = response.json()
            raise RuntimeError(f"Unable to save user: Status: {status}. Error: {error}")

        sleep(0.1)
