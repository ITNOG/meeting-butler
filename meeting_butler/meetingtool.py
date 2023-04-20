"""
Methods to interact with NIX.CZ's meetingtool
"""

import json
import logging

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

    for start in range(0, len(users), 15):
        stop = start + 15
        data = [
            {
                "firstName": user["name"],
                "lastName": user["surname"],
                "company": user["company"],
                # Email address has to be lowercase
                "mail": user["email"].lower(),
                "jobTitle": user["title"],
                "asn": user["asn"],
                "countryCode": user["country"]
            }
            for user in users[start:stop]
        ]

        LOGGER.debug("Importing the following users: %s", data)
        request = requests.post(url, data=json.dumps(data), headers=headers, timeout=30)

        status = request.status_code
        if status != 200:
            raise RuntimeError(f"Unable to save users: {status.content}")
