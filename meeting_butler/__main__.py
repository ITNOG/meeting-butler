"""
Main entrypoint for the package.
"""

import argparse
import logging
from time import sleep

from meeting_butler.meeting_butler import sync
from meeting_butler.settings import Settings


def __main__() -> None:
    """
    Main application entrypoint.
    Stats an infiite loop executing sync() every `sync_every` seconds
    """
    settings = Settings()

    logging.basicConfig()
    logger = logging.getLogger("meeting_butler")

    if settings.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debugging is ON")
    else:
        logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser(
        prog="meeting_butler",
        description="Takes care of background tasks pertained to meeting and registrations",
    )
    parser.add_argument("email_regex", metavar="REGEX", type=str, help="Only process attendees whos email address matches with this regex", default=False)
    args = parser.parse_args()

    while True:
        sync(
            settings.eventbrite_event,
            settings.eventbrite_token,
            settings.meetingtool_hostname,
            settings.meetingtool_token,
            settings.cache_filename,
            args.email_regex,
        )

        sleep(settings.sync_every)


if __name__ == "__main__":
    __main__()
