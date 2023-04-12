import json
import logging

import requests

from meeting_butler.user import User

LOGGER = logging.getLogger(__name__)


def register_users(hostname: str, token: str, users: list[User]) -> None:
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
                "mail": user["email"],
                "jobTitle": user["title"],
                "asn": user["asn"],
            }
            for user in users[start:stop]
        ]

        LOGGER.debug("Importing the following users: %s", data)
        request = requests.post(url, data=json.dumps(data), headers=headers, timeout=30)

        status = request.status_code
        if status != 200:
            raise RuntimeError(f"Unable to save users: {status.content}")
