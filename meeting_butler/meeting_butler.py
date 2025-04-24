"""
Methods implementing the application logic
"""

import logging
import os
import re
from typing import Optional

from meeting_butler import eventbrite, formbuilder, meetingtool, pretino
from meeting_butler.cache import Cache
from meeting_butler.user import User

LOGGER = logging.getLogger(__name__)


def sync(
    meetingtool_hostname: str,
    meetingtool_token: str,
    source_settings: Optional[dict],
    data_source: str = "pretino",
    cache_filename: Optional[os.PathLike] = False,
    email_regex: str = False,
) -> list[User]:
    """
    Synchronizes meetingtool users with Eventbrite users

    Arguments:
    ----------
    meetingtool_hostname: str
        Meetingtool instance hostname
    meetingtool_token: str
        Meetingtool API token
    source_settings: dict
        Dictionary with source specific settings
    data_source: str
        Either 'formbuilder' or 'meetingtool'.
    cache_filename: Optional[os.PathLike]
        File name and path to the local cache. False means cache.db
        Default: False
    email_regex: str
        Regex. If not false, email addresses not matching with it are discarded
        Default False

    Returns:
    --------
    list[User]: List of newly added users
    """
    LOGGER.info("Sync started")

    new_users = []

    cache = Cache(cache_filename)
    if data_source == "eventbrite":
        source_users = eventbrite.get_registered_users(
            source_settings["event"], source_settings["token"]
        )
    elif data_source == "formbuilder":
        source_users = formbuilder.get_registered_users(source_settings["url"])
    elif data_source == "pretino":
        source_users = pretino.get_registered_users(
            source_settings["url"], source_settings["token"]
        )
    else:
        raise RuntimeError(f"Unsupported data source: {data_source}")

    with Cache(cache_filename) as cache:
        for user in source_users:
            if email_regex and not re.search(email_regex, user["email"], re.IGNORECASE):
                continue
            if user["email"] not in cache:
                new_users.append(user)

        LOGGER.info("Found %d new users", len(new_users))
        LOGGER.debug("New users: %s", new_users)

        meetingtool.register_users(meetingtool_hostname, meetingtool_token, new_users)
        for new_user in new_users:
            cache[new_user["email"]] = new_user

    LOGGER.info("Sync completed")

    return new_users
